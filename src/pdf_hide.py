#!/usr/bin/python3
import sys
import select
import argparse
import getpass

import logger
import pdf_algo

#
#
#
# PDF HIDE
#

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
#
# Copyright (C) 2013 Nicolas Canceill
#

#
# pdf_hide.py
__version__ = "0.0a"
#
# This is a steganographic tool for hiding data in PDF files
#
# Written by Nicolas Canceill
# Last updated on May 6, 2013
# Hosted at https://github.com/ncanceill/pdf_hide
#

#
#
#
# SCRIPT
#

def main():
	# CLI
	parser = argparse.ArgumentParser(prog="pdf_hide", formatter_class=argparse.RawDescriptionHelpFormatter,
						description=logger.MSG_DESC, epilog=logger.MSG_LICENSE)
	subparsers = parser.add_subparsers(title="actions", dest="action",
									   help="action to execute")
	# CLI - General
	parser.add_argument("filename",
						help="PDF file (may be compressed) to use as input")
	parser.add_argument("-o", "--output", dest="output", default="out.pdf_hide",
						help="use FILENAME as the output file", metavar="FILENAME")
	parser.add_argument("-k", "--key", dest="key",
						help="use KEY as the stego-key", metavar="KEY")
	# CLI - Embedding
	parser_embed = subparsers.add_parser("embed", help="Embed message inside PDF file")
	parser_embed.add_argument("data", type=argparse.FileType(),
						help="the data file to embed (or stdin)")
	parser_embed.add_argument("--no-random", action="store_true", dest="norandom", default=False,
						help="do not embed random values, keep original ones")
	# CLI - Extracting
	parser_extract = subparsers.add_parser("extract", help="Extract message from PDF file")
	# CLI - Options
	group_options = parser.add_argument_group("algorithm options", "use these options to tune the algorithm")
	group_options.add_argument("-n", "--nbits", dest="nbits", action="store", type=int, default=4,
						help="use NBITS as the number of bits to use for numerals", metavar="NBITS")
	group_options.add_argument("-r", "--redundancy", dest="red", action="store", type=float, default=0.1,
						help="use RED as the redundancy parameter (strictly between 0 and 1)", metavar="RED")
	# CLI - Improvements #TODO: clean that up
	parser.add_argument("-i", "--improve", action="store_true", dest="improve", default=False,
						help="use algo improvements")
	parser.add_argument("--custom-range", action="store_true", dest="customrange", default=False,
						help="use data in [-450,-250] without -333 and -334 (ignored with original algo, should always be used in combination with --no-random when embedding)")
	# CLI - Verbosity
	group_verb = parser.add_mutually_exclusive_group()
	group_verb.add_argument("-v", "--verbose", action="count", dest="verbose", default=0,
						help="set verbosity level")
	group_verb.add_argument("-q", "--quiet", action="store_const", dest="verbose", const=-1,
						help="force quiet output")
	# CLI - Version
	group_version = parser.add_argument_group("version")
	group_version.add_argument("--version", action="version", version=logger.MSG_VERSION)
	args = parser.parse_args()
	# Log
	rl = logger.rootLogger(args.verbose)
	# Exec
	if args.verbose >= 0:
		rl.print_splash()
	if args.action == "embed":
		if args.key == None:
			args.key = getpass.getpass("Please enter stego-key: ")
		ps = pdf_algo.PDF_stego(args.filename,rl,output=args.output,improve=args.improve,red=args.red,nbits=args.nbits,customrange=args.customrange)
		result = ps.embed(args.data.read(),args.key,norandom=args.norandom)
		if args.verbose >= 0:
			rl.print_discl()
		if result > 0:
			exit(0)
		exit(result)
	elif args.action == "extract":
		if args.key == None:
			args.key = getpass.getpass("Please enter derived-key: ")
		ps = pdf_algo.PDF_stego(args.filename,rl,output=args.output,improve=args.improve,red=args.red,nbits=args.nbits,customrange=args.customrange)
		result = ps.extract(args.key)
		if args.verbose >= 0:
			rl.print_discl()
		exit(result)

if __name__ == '__main__':
    main()
