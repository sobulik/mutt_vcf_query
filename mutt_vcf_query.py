#!/usr/bin/env python3

"""Mutt utility to search through vCard records"""

import sys
import argparse
import re
import os

class VcfParser():
    """vCard parser and accessor"""
    def __init__(self, fileName):
        # compile regular expressions
        self.__vcf_name = re.compile("^FN:(.*)$")
        self.__vcf_mail = re.compile(r"^(item1.)?EMAIL[^:]*:(.*)$")

        self.__vcf_records = []
        with open(fileName, "r") as vcf_file:
            recording = False
            for line in vcf_file:
                if not recording:
                    if "BEGIN:VCARD" in line:
                        recording = True
                        vcf_record = {}
                else:
                    if "END:VCARD" in line:
                        recording = False
                        self.__vcf_records.append(vcf_record)
                    else:
                        if not "fullName" in vcf_record:
                            match = self.__vcf_name.match(line)
                            if match is not None:
                                vcf_record["fullName"] = match.group(1)
                        match = self.__vcf_mail.match(line)
                        if match is not None:
                            if not "mails" in vcf_record:
                                vcf_record["mails"] = []
                            vcf_record["mails"].append(match.group(2))

    def get_records(self):
        """get vCard records"""
        return self.__vcf_records

    def lookup_name_and_mail(self, stub):
        """look up vCard records for stub"""
        stub = stub.lower()
        hits = []
        for vcf_record in self.get_records():
            if "fullName" in vcf_record and "mails" in vcf_record and len(vcf_record["mails"]) > 0:
                if stub in vcf_record["fullName"].lower():
                    for mail in vcf_record["mails"]:
                        hits.append((vcf_record["fullName"], mail))
                else:
                    for mail in vcf_record["mails"]:
                        if stub in mail.lower():
                            hits.append((vcf_record["fullName"], mail))
        return hits

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="vCard file")
    parser.add_argument("stub", help="string to search")
    args = parser.parse_args()

    if os.path.isfile(args.file):
        matches = VcfParser(args.file).lookup_name_and_mail(args.stub)
        if len(matches) > 0:
            print("%d match(es) found" % len(matches))
            for item in sorted(matches):
                print("%s\t%s" % (item[1], item[0]))
            sys.exit(0)
        else:
            print("No matches found")
            sys.exit(1)
    else:
        print("File %s doesn't exist" % (args.file), file=sys.stderr)
        sys.exit(1)
