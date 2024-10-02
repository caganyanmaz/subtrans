from argparse import ArgumentParser
from googletrans import Translator
import srt


def main():
    argument_parser = ArgumentParser(prog="subtrans")
    argument_parser.add_argument("filename")
    argument_parser.add_argument("--fr", "--from", type=str, default="en")
    argument_parser.add_argument("--to", type=str, default="tr") 
    argument_parser.add_argument("-o", "--output")

    args = argument_parser.parse_args()
    
    if args.output is None:
        args.output = create_default_output_filename(args.filename, args.fr, args.to)
    translate_file(args.filename, args.output, args.fr, args.to)


def translate_file(in_file, out_file, fr, to):
    with open(in_file, "r") as file:
        input_data = file.read()
    output_data = translate_data(input_data, fr, to)
    with open(out_file, "w") as file:
        file.write(output_data)


def translate_data(data, fr, to):
    translator = Translator()
    subtitles = list(srt.parse(data))
    subtitle_count = len(subtitles)
    for i, subtitle in enumerate(subtitles):
        print(f"Translated {i}/{subtitle_count} subtitles...")
        subtitle.content = translator.translate(subtitle.content, src=fr, dest=to).text
    return srt.compose(sub)


def create_default_output_filename(filename, fr, to):
    extension_without_lang = ".srt"
    extension_with_lang    = "." +  fr + extension_without_lang
    prefix = filename
    if is_string_containing_suffix(filename, extension_with_lang):
        prefix = filename[:-len(extension_with_lang)]
    elif is_string_containing_suffix(filename, extension_without_lang):
        prefix = filename[:-len(extension_without_lang)]
    return prefix + "." + to + ".srt"


def is_string_containing_suffix(string, suffix):
    print(string, suffix, string[-len(suffix):])
    return len(string) >= len(suffix) and string[-len(suffix):] == suffix


if __name__ == "__main__":
    main()

