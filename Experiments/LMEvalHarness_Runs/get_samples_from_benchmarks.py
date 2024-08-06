# Run:
# python get_samples_from_benchmarks.py --samples_folder aya-23-8b-hellaswag_with_okapi_with_template/aya-23-8B --output hellaswag_multilingual
#
#

import os, argparse
import pandas as pd
from tqdm import tqdm

import logging
from tqdm.contrib.logging import logging_redirect_tqdm

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main(args):
    samples_dir = args.samples_folder
    output_file = args.output
    prefix = args.file_prefix

    files = os.listdir(samples_dir)

    # # To collect all samples into one single file
    # file_paths = Need to redefine
    # benchmark_arguments = []
    # for file in tqdm(file_paths):
    #     benchmark_arguments += get_arguments_from_file(file)
    #
    # df = pd.concat(benchmark_arguments)
    # df.to_feather(f"{output_file}.feather")

    # For individual sample files
    output_folder = output_file
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in tqdm(files):
        if not file.startswith(prefix):
            continue

        arguments = get_arguments_from_file(os.path.join(samples_dir, file))
        df = pd.concat(arguments)

        # Filename split assuming there are no extra dots in the filename, change if there are
        df.to_feather(f"{output_folder}/{file.split('.')[0]}.feather")


def get_arguments_from_file(file_path):
    # TODO A faster vectorized implementation
    arguments = []

    with logging_redirect_tqdm():
        LOG.info(f"Processing file {file_path}")

    df = pd.read_json(file_path, lines=True)

    df = df[["doc_id", "arguments"]]

    def process(b):
        doc_id = b.doc_id
        out = pd.json_normalize(b.arguments)
        out["doc_id"] = doc_id
        out = out.drop(columns=["gen_args_1.arg_0", "gen_args_2.arg_0", "gen_args_3.arg_0"])

        arguments.append(out)

    df.apply(lambda x: process(x), axis=1)

    return arguments


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--samples_folder', type=str, help="Path/to/benchmark/samples/folder")
    parser.add_argument('--file_prefix', default="samples_", type=str, help="File name prefix")
    parser.add_argument('--output', type=str, help="Path/to/output/file")

    args = parser.parse_args()

    main(args)
