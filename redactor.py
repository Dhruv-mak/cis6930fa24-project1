import os
import argparse
import sys
import glob
import spacy
from spacy.language import Language
from spacy.tokens import Doc, Token
from redactors.date import date_redactor
from redactors.phone import phone_redactor
from redactors.name import name_redactor
from redactors.address import address_redactor
from redactors.concept import concept_redactor
from names_dataset import NameDataset
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex

def custom_tokenizer(nlp):
    infixes = [r"[_@.:]"]
    infix_re = compile_infix_regex(tuple(infixes))

    return Tokenizer(nlp.vocab,
                     prefix_search=nlp.tokenizer.prefix_search,
                     suffix_search=nlp.tokenizer.suffix_search,
                     infix_finditer=infix_re.finditer,
                     token_match=nlp.tokenizer.token_match)

def redact_doc(doc: Doc) -> str:
    redacted_text = []
    for token in doc:
        if token._.get("redact"):
            redacted_text.append("█" * len(token.text))
        else:
            redacted_text.append(token.text_with_ws)
    return "".join(redacted_text)


def process_file(nlp: Language, input_file: str, output_file: str, stream) -> None:
    try:
        with open(input_file, "r") as f:
            text = f.read()
        doc = nlp(text)
        redacted_text = redact_doc(doc)
        with open(output_file, "w") as f:
            f.write(redacted_text)
    except IOError as e:
        print(f"Error reading or writing file: {e}", file=sys.stderr)


def main(params: argparse.Namespace) -> None:
    if not os.path.exists(params.output):
        os.makedirs(params.output)

    Token.set_extension("redact", default=False, force=True)

    if params.stats == "stdout":
        stream = sys.stdout
    elif params.stats == "stderr":
        stream = sys.stderr
    else:
        stream = open(params.stats, "a")

    nlp = spacy.load("en_core_web_trf")
    nlp.tokenizer = custom_tokenizer(nlp)
    Doc.set_extension("stream", default=stream, force=True)
    Doc.set_extension("concept", default=params.concept, force=True)

    if params.phones:
        nlp.add_pipe("phone_redactor", last=True)
    if params.dates:
        nlp.add_pipe("date_redactor", last=True)
    if params.names:
        nlp.add_pipe("name_redactor", last=True)
    if params.addresses:
        nlp.add_pipe("address_redactor", last=True)
    if params.concept:
        nlp.add_pipe("concept_redactor", last=True)


    for input_file in params.input:
        Doc.set_extension("input_file", default=input_file, force=True)
        output_file = os.path.join(
            params.output, os.path.basename(input_file) + ".redacted"
        )
        process_file(nlp, input_file, output_file, stream)
    if params.stats not in ["stdout", "stderr"]:
        stream.close()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Redaction Program",
        description="Redact sensitive information from text files like names, dates, phone numbers, addresses, and concepts",
    )
    parser.add_argument("--names", action="store_true", help="Redact names")
    parser.add_argument("--dates", action="store_true", help="Redact dates")
    parser.add_argument("--phones", action="store_true", help="Redact phone numbers")
    parser.add_argument("--addresses", action="store_true", help="Redact addresses")
    parser.add_argument("--concept", action="append", help="Redact concepts")
    parser.add_argument(
        "--input", type=str, help="glob pattern for input files", required=True
    )
    parser.add_argument("--output", type=str, help="output directory", required=True)
    parser.add_argument("--stats", type=str, help="output file for stats")

    args = parser.parse_args()
    args.input = glob.glob(os.path.expanduser(args.input))
    return args


if __name__ == "__main__":
    args = parse_arguments()
    main(args)