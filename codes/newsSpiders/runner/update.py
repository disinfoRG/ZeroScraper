import os


def run(args, defaults):
    if args.delay is not None:
        delay = args.delay
    else:
        delay = defaults["delay"]
    if args.ua is not None:
        ua = args.ua
    else:
        ua = defaults["ua"]

    os.system(
        f"scrapy crawl update_contents \
                -s DOWNLOAD_DELAY={delay} \
                -s USER_AGENT='{ua}'"
    )
