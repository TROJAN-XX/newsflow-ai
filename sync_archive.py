import os
import shutil


SOURCE = os.path.join(
    "data",
    "news_archive.json"
)

DESTINATION = os.path.join(
    "website",
    "public",
    "data",
    "news_archive.json"
)


def main():

    if not os.path.exists(SOURCE):

        print(
            "Archive not found:"
        )

        print(SOURCE)

        return

    os.makedirs(
        os.path.dirname(DESTINATION),
        exist_ok=True
    )

    shutil.copy2(
        SOURCE,
        DESTINATION
    )

    print(
        "Archive synchronized successfully."
    )

    print(
        f"Source: {SOURCE}"
    )

    print(
        f"Destination: {DESTINATION}"
    )


if __name__ == "__main__":
    main()