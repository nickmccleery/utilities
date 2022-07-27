import json
from pathlib import Path
from argparse import ArgumentParser


def process_file(input_filepath: Path, output_filepath: Path):
    """
    Processes Postman collection export files, yielding a new collection
    JSON file with requests sorted alphabetically.

    Arguments:
        input_filepath {Path} -- Filepath for sort target input collection.
        output_filepath {Path} -- Filepath for sorted export collection.

    Raises:
        AttributeError: When input collection fails basic validation.
    """
    # Load data.
    with open(input_filepath) as file:
        collection = json.load(file)

    # Some very light schema validation.
    keys = collection.keys()
    if 'item' not in keys or 'info' not in keys:
        raise AttributeError(
            "Collection does not meet the expected format."
        )

    # Run the sort.
    collection['item'] = sorted(collection['item'], key=lambda x: x['name'])

    # Export.
    with open(output_filepath, 'w') as f:
        json.dump(
            collection,
            f,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )

    # Report.
    n_requests = len(collection['item'])
    message = (
        f"Processing of {n_requests} requests completed successfully. Output "
        f"file: {output_filepath}"
    )

    return(message)


def run():
    """
    Entry point function; parses command line arguments and initiates 
    processing.

    Raises:
        FileNotFoundError: When input file could not be found.
        Exception: When processing fails.
    """
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--inputfile",
        dest="input_filepath",
        help="Postman collection export JSON file to be processed.",
    )

    parser.add_argument(
        "-o",
        "--outputfile",
        dest="output_filepath",
        help="Output (sorted) collection filepath.",
    )

    args = parser.parse_args()

    # Validate input file.
    input_filepath = Path(args.input_filepath)
    if not input_filepath.is_file():
        raise FileNotFoundError(
            "Could not find specified input collection."
        )

    output_filepath = Path(args.output_filepath)

    try:
        message = process_file(
            input_filepath=input_filepath,
            output_filepath=output_filepath
        )
        print(message)
    except Exception as e:
        raise Exception(
            f"Collection processing failed: {str(e)}"
        )

    return


if __name__ == "__main__":
    run()
