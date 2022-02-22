import csv
import sys
import os.path
import json
from generatorcore import refdatatools
from generatorcore import refdata
from generatorcore import makeentries


def cmd_data_normalize(args):
    with open(args.file, "r") as fp:
        rows = list(csv.reader(fp))
    with open(args.file, "w") as fp:
        writer = csv.writer(fp, lineterminator="\n")
        for row in rows:
            writer.writerow(row)


def cmd_data_is_production(args):
    ds = refdatatools.DataDirStatus.get(refdatatools.datadir())
    # TODO: Add a verbose option that prints a json of DataDirStatus
    if not ds.is_good():
        exit(1)


def cmd_data_lookup(args):
    ags = args.ags
    ags_dis = ags[:5] + "000"  # This identifies the administrative district (Landkreis)
    ags_sta = ags[:2] + "000000"  # This identifies the federal state (Bundesland)

    def bold(s):
        print(f"\033[1m{s}\033[0m")

    def print_lookup(name, lookup_fn, key):
        bold(name)
        try:
            record = lookup_fn(key)
        except Exception as e:
            record = None

        if record is None:
            print("", "MISSING", sep="\t")
        else:
            print(record)
        print()

    data = refdata.RefData.load(fix_missing_entries=args.fix_missing_entries)

    by_ags = [
        ("area", data.area),
        ("area_kinds", data.area_kinds),
        ("buildings", data.buildings),
        ("population", data.population),
        ("renewable_energy", data.renewable_energy),
        ("flats", data.flats),
        ("traffic", data.traffic),
    ]

    by_dis = [
        ("destatis", data.destatis),
    ]

    by_sta = [
        ("nat_agri", data.nat_agri),
        ("nat_organic_agri", data.nat_organic_agri),
        ("nat_energy", data.nat_energy),
        ("nat_res_buildings", data.nat_res_buildings),
    ]

    description = data.ags_master().get(ags, "MISSING IN MASTER")

    bold(f"{ags} {description} (commune level data)")
    bold("---------------------------------------------------------------")
    print()
    for (name, lookup_fn) in by_ags:
        print_lookup(name, lookup_fn, key=ags)

    bold(f"{ags_dis} (administrative district level data)")
    bold("--------------------------------------------------")
    print()
    for (name, lookup_fn) in by_dis:
        print_lookup(name, lookup_fn, key=ags_dis)

    bold(f"{ags_sta} (federal state level data)")
    bold("--------------------------------------------------")
    print()
    for (name, lookup_fn) in by_sta:
        print_lookup(name, lookup_fn, key=ags_sta)


def cmd_data_checkout(args):
    def update_existing(
        repo: refdatatools.PUBLIC_OR_PROPRIETARY, *, current: str, wanted: str
    ):
        if current == wanted:
            if not freshly_cloned:
                print(
                    f"{repo} already contains a checkout of {wanted} -- not touching it",
                    file=sys.stderr,
                )
        else:
            print(f"switching {repo} from {current} to {wanted}")
            # First switch to main before pulling -- this has the least chance of causing
            # trouble as we should merge on github
            refdatatools.checkout(datadir, repo, "main")
            # refdatatools.pull uses --ff-only
            refdatatools.pull(datadir, repo, pa_token=args.pat)
            # Now we should have all changes and can switch to whatever the production file
            # wants
            refdatatools.checkout(datadir, repo, wanted)

    datadir = refdatatools.datadir()
    public_dir = os.path.join(datadir, "public")
    proprietary_dir = os.path.join(datadir, "proprietary")
    freshly_cloned = False

    # Clone the repos if there is nothing at all
    if not os.path.exists(public_dir) and not os.path.exists(proprietary_dir):
        print(
            "Looks like there is no checkout at all yet -- cloning for you",
            file=sys.stderr,
        )
        refdatatools.clone(datadir, "public", pa_token=args.pat)
        refdatatools.clone(datadir, "proprietary", pa_token=args.pat)
        freshly_cloned = True

    # now figure out the current state
    status = refdatatools.DataDirStatus.get(datadir)

    # make sure we are not causing data loss
    if not status.public_status.is_clean or not status.proprietary_status.is_clean:
        print(
            "There uncommitted changes or untracked files in at least one data repository. Fix that first."
        )
        exit(1)

    # Alright now pull and checkout the wanted hashes
    update_existing(
        "public", current=status.public_status.rev, wanted=status.production.public
    )
    update_existing(
        "proprietary",
        current=status.proprietary_status.rev,
        wanted=status.production.proprietary,
    )


def cmd_data_entries_user_overrides_generate_defaults(args):
    data = refdata.RefData.load()
    result = []
    good = 0
    errors = 0
    crazy_errors = 0
    with open("errors.txt", "w") as error_file, open(
        "crazy-errors.txt", "w"
    ) as crazy_error_file:

        for (ags, description) in list(data.ags_master().items()):
            try:
                entries = makeentries.make_entries(data, ags, 2035)
                default_values = {
                    k: v
                    for (k, v) in entries.items()
                    if k in makeentries.USER_OVERRIDABLE_ENTRIES
                }
                default_values["city"] = description
                result.append(default_values)
                good = good + 1
            except refdata.LookupFailure as e:
                errors = errors + 1
                print(ags, repr(e), sep="\t", file=error_file)
            except Exception as e:
                crazy_errors = crazy_errors + 1
                print(ags, repr(e), sep="\t", file=crazy_error_file)

            sys.stdout.write(
                f"\rOK {good:>5}    BAD {errors:>5}  CRAZY {crazy_errors:>5}"
            )
    with open("output.json", "w") as output_file:
        json.dump(result, indent=4, fp=output_file)
