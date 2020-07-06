#!/usr/bin/env python3

import argparse
import re
from pathlib import Path
import logging
import coloredlogs
import progressbar

import pandas as pd


def parse_report(lines):
    out = {}
    for line in lines[2:9]:
        match = re.search(
            r"^\s*?(?P<class>\d)\s+?(?P<precision>\d+?\.\d+?)\s+?(?P<recall>\d+?\.\d+?)\s+?(?P<f1>\d+?\.\d+?)\s+?(?P<support>\d+?)$",
            line.strip()
        )
        out[f"class_{match.group('class')}"] = {
            'precision': float(match.group('precision')),
            'recall': float(match.group('recall')),
            'f1': float(match.group('f1')),
            'support': int(match.group('support')),
        }

    match = re.search(
        r"^\s*?accuracy\s+?(?P<accuracy>\d+?\.\d+?)\s+?(?P<support>\d+?)$",
        lines[10].strip()
    )
    out['accuracy'] = float(match.group('accuracy'))
    out['support'] = int(match.group('support'))
    match = re.search(
        r"^\s*?(?P<type>.*?)\s+?(?P<precision>\d+?\.\d+?)\s+?(?P<recall>\d+?\.\d+?)\s+?(?P<f1>\d+?\.\d+?)\s+?(?P<support>\d+?)$",
        lines[11].strip()
    )
    out['avg_precision'] = float(match.group('precision'))
    out['avg_recall'] = float(match.group('recall'))
    out['avg_f1'] = float(match.group('f1'))
    match = re.search(
        r"^\s*?(?P<type>.*?)\s+?(?P<precision>\d+?\.\d+?)\s+?(?P<recall>\d+?\.\d+?)\s+?(?P<f1>\d+?\.\d+?)\s+?(?P<support>\d+?)$",
        lines[12].strip()
    )
    out['weithed_avg_precision'] = float(match.group('precision'))
    out['weithed_avg_recall'] = float(match.group('recall'))
    out['weithed_avg_f1'] = float(match.group('f1'))
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'models',
        help="the directory containing the models' reports",
    )
    parser.add_argument(
        '--out', '-o',
        help="the output filename or path (without extension)",
        default='final-report'
    )
    parser.add_argument(
        '--format', '-f',
        help="the output format (default: csv)",
        choices=['xlsx', 'csv'],
        default='csv'
    )
    parser.add_argument(
        '--verbose', '-v',
        help="set output to verbose",
        action='store_true'
    )
    args = parser.parse_args()

    coloredlogs.install(
        level=logging.INFO if args.verbose else logging.WARNING,
        milliseconds=True
    )

    base = Path(args.models)

    data = []

    for cv_file in progressbar.progressbar(list(base.rglob('*-cv.csv')), redirect_stderr=True, redirect_stdout=True):
        logging.info("Reading: %s", str(cv_file).replace('\\', '/'))
        match = re.search(
            r"^(?:.*?/)?models/w(?P<width>\d+?)/(?P<half>\w+?)/(?P<model>.+?)/(?P<emotion>.*?)-cv\.csv$",
            str(cv_file).replace('\\', '/')
        )
        df = pd.read_csv(cv_file, index_col=0)

        report_file = cv_file.parent / f"{match.group('emotion')}-report.txt"
        with open(report_file, 'r') as f:
            report = pd.json_normalize(parse_report(f.readlines()), sep='_')\
                .to_dict(orient='records')[0]

        data.append({
            'model': match.group('model'),
            'width': int(match.group('width')),
            "half": match.group('half'),
            "emotion": match.group('emotion'),
            "CV_avg_fit_time": df['fit_time'].mean(),
            "CV_std_fit_time": df['fit_time'].std(),
            "CV_avg_score_time": df['score_time'].mean(),
            "CV_std_score_time": df['score_time'].std(),
            "CV_avg_test_score": df['test_score'].mean(),
            "CV_std_test_score": df['test_score'].std(),
            **report
        })

    final = pd.DataFrame(data).sort_values(
        by=['model', 'width', 'half', 'emotion']
    )

    # Nota: le medie pesate di precision, recall ed F1 score sono calcolate
    # utilizzando i valori support come pesi.

    try:
        if args.format == 'xlsx':
            logging.info("Saving final Excel file to '%s'", f"{args.out}.{args.format}")
            final.to_excel(f"{args.out}.{args.format}", index=False)
        elif args.format == 'csv':
            logging.info("Saving final CSV file to '%s'", f"{args.out}.{args.format}")
            final.to_csv(f"{args.out}.{args.format}", index=False)
        else:
            raise argparse.ArgumentError("Format is not recognized")
    except Exception as err:
        logging.fatal(
            "%s%s",
            type(err).__name__,
            f': {str(err)}' if str(err) else ''
        )
