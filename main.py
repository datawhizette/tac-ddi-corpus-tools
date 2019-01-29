import argparse
import logging
import os

from tac_tools.conll_results_to_xml import conll_to_xml
from tac_tools.test_xml_to_conll_converter import convert_xml_to_conll_format_test
from tac_tools.train_xml_to_conll_converter import convert_xml_to_conll_format

if __name__ == "__main__":

    parser = argparse.ArgumentParser ( )

    subparsers = parser.add_subparsers (title="Sub-commands", description="Valid sub-commands",
                                        help="Valid sub-commands", dest="subparser_name")

    # Convert train files to conll
    parser_conll_train = subparsers.add_parser ('convert_train',
                                                help="Convert the whole directory of training XML files to "
                                                     "CoNLL format")
    parser_conll_train.add_argument ("--input_path", help="Input corpus path", dest="input_path", type=str,
                                     required=True)
    parser_conll_train.add_argument ("--output_file", help="Output conll file in txt format", dest="output_file",
                                     type=str,
                                     required=True)

    # Convert test files to conll
    parser_conll_test = subparsers.add_parser ('convert_test', help="Convert the whole directory of test XML files to "
                                                                    "CoNLL format")
    parser_conll_test.add_argument ("--input_path", help="Input corpus path", dest="input_path", type=str,
                                    required=True)
    parser_conll_test.add_argument ("--output_file", help="Output conll file in txt format", dest="output_file",
                                    type=str,
                                    required=True)

    # Convert result conll files to xml
    parser_xml = subparsers.add_parser ('convert_results', help="Convert the whole directory of test XML files to "
                                                                "CoNLL format")
    parser_xml.add_argument ("--input_path", help="Path where test files in XML format are located (without tags)",
                             dest="input_path", type=str,
                             required=True)
    parser_xml.add_argument ("--input_file", help="Test data without tags in CoNLL format", dest="input_file", type=str,
                             required=True)
    parser_xml.add_argument ("--trigger_file", help="Input trigger results file in txt format", dest="trigger_file",
                             type=str,
                             required=True)
    parser_xml.add_argument ("--specificints_file", help="Input specificInteraction results file in txt format",
                             dest="specificints_file", type=str,
                             required=True)
    parser_xml.add_argument ("--output_path", help="Output path, where to write the resulting XML files to",
                             dest="output_path", type=str,
                             required=True)

    args = parser.parse_args ( )

    if args.subparser_name == "convert_train":

        logging.basicConfig (level=logging.INFO, format='%(asctime)s %(message)s')

        logging.info ("Converting files: {}".format (os.path.abspath (args.input_path)))
        logging.info ("* Target file: {}".format (os.path.abspath (args.output_file)))

        convert_xml_to_conll_format (args.input_path, args.output_file)

    elif args.subparser_name == "convert_test":

        logging.basicConfig (level=logging.INFO, format='%(asctime)s %(message)s')

        logging.info ("Converting files: {}".format (os.path.abspath (args.input_path)))
        logging.info ("* Target file: {}".format (os.path.abspath (args.output_file)))

        convert_xml_to_conll_format_test (args.input_path, args.output_file)

    elif args.subparser_name == "convert_results":

        logging.basicConfig (level=logging.INFO, format='%(asctime)s %(message)s')

        logging.info (" Test path before converting in XML format: {}".format (os.path.abspath (args.input_path)))
        logging.info ("* Test file before converting in CoNLL format: {}".format (os.path.abspath (args.input_file)))
        logging.info ("* File to convert (triggers): {}".format (os.path.abspath (args.trigger_file)))
        logging.info ("* File to convert (specific interactions): {}".format (os.path.abspath (args.specificints_file)))
        logging.info ("* Result path: {}".format (os.path.abspath (args.output_path)))

        conll_to_xml (args.input_path, args.input_file, args.trigger_file, args.specificints_file, args.output_path)
