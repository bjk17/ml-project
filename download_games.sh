#!/usr/bin/env bash

OUTPUT_DIR="games"
mkdir -p $OUTPUT_DIR

for DATE_STAMP in 2010 2011 2012 2013 2014 2015 2016 2017 201801 201802 201803 201804 201805 201806 201807 201808 201809; do
    PGN_FILE="ficsgamesdb_${DATE_STAMP}_standard2000_movetimes.pgn"
    ZIPPED_FILE="${PGN_FILE}.bz2"
    if [ -f "${OUTPUT_DIR}/$PGN_FILE" ]; then
        echo "OK: PGN file exists for DATE_STAMP $DATE_STAMP";
    else
        echo "INFO: Downloading and extracting $ZIPPED_FILE from https://misc.bjk.is/ml/games/ ..."
        wget --no-check-certificate https://misc.bjk.is/ml/games/${ZIPPED_FILE} -P $OUTPUT_DIR/
        bzip2 -d ${OUTPUT_DIR}/${ZIPPED_FILE} &
    fi
done

wait # for bzip processes in background

