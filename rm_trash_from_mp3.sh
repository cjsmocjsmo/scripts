find . -name "*.flac" -exec metaflac --remove-tag=DATE \
	--remove-tag='PUBLISHER' \
	--remove-tag='ISRC' \
	--remove-tag='BARCODE' \
	--remove-tag='ITUNESADVISORY' \
	--remove-tag='LYRICS' \
	--remove-tag='COPYRIGHT' \
	--remove-tag='ENCODED-BY' \
	--remove-tag='ENCODER' \
	--remove-tag='ENCODERSETTINGS' \
	--remove-tag='SOURCEMEDIA' \
	--remove-tag='RELEASECOUNTRY' \
	--remove-tag='COMPOSER' \
	--remove-tag='LENGTH' \
	--remove-tag='ALBUMARTIST' \
	--remove-tag='DYNAMIC RANGE' \
  	--remove-tag='ALBUM DYNAMIC RANGE' \
  	--remove-tag='REPLAYGAIN_TRACK_GAIN' \
  	--remove-tag='REPLAYGAIN_TRACK_PEAK' \
  	--remove-tag='REPLAYGAIN_ALBUM_GAIN' \
  	--remove-tag='REPLAYGAIN_ALBUM_PEAK' \
	--remove-tag='REPLAYGAIN_REFERENCE_LOUDNESS' \
  	--remove-tag='ACCURATERIPID' \
  	--remove-tag='ACCURATERIPCRC' \
  	--remove-tag='ACCURATERIPDISCID' \
  	--remove-tag='ACCURATERIPCOUNT' \
  	--remove-tag='ACCURATERIPCOUNTALLOFFSETS' \
  	--remove-tag='ACCURATERIPTOTAL' \
  	--remove-tag='CTDBDISCCONFIDENCE' \
  	--remove-tag='CTDBTRACKCONFIDENCE' \
  	--remove-tag='COMMENT' \
  	--remove-tag='ALBUM ARTIST' \
  	--remove-tag='ALBUMARTIST' \
  	--remove-tag='LABEL' \
  	--remove-tag='DISCID' \
  	--remove-tag='RELEASE DATE' \
  	--remove-tag='RELEASECOUNTRY' \
  	--remove-tag='PUBLISHER' \
  	--remove-tag='ORGANIZATION' \
  	--remove-tag='MCN' \
  	--remove-tag='CDTOC' \
  	--remove-tag='ORIGYEAR' \
	--remove-tag='ORIGINALYEAR' \
  	--remove-tag='LABELNO' \
	--remove-tag='ALBUMARTISTSORT' \
	--remove-tag='ARTISTSORT' \
	--remove-tag='CATALOGNUMBER' \
	--remove-tag='extragenre' \
	--remove-tag='MEDIA' \
	--remove-tag='MUSICBRAINZ_TRACKID' \
	--remove-tag='MUSICBRAINZ_RELEASEID' \
	--remove-tag='MUSICBRAINZ_RELEASEGROUPID' \
	--remove-tag='MUSICBRAINZ_RELEASETRACKID' \
	--remove-tag='ARTISTS' \
	--remove-tag='MUSICBRAINZ_ALBUMARTISTID' \
	--remove-tag='MUSICBRAINZ_ALBUMID' \
	--remove-tag='MUSICBRAINZ_ARTISTID' \
	--remove-tag='ORIGINALDATE' \
	--remove-tag='RELEASESTATUS' \
	--remove-tag='RELEASETYPE' \
	--remove-tag='SCRIPT' \
	--remove-tag='WORK' {} +

rename -n 's/^(\d+)[.\-\s]+\s*(.*?)\.flac$/ my $num = $1; my $t = $2; $t =~ s{ }{_}g; "1_${num}_-_Van_Halen_-_A_Differnt_Kind_Of_Truth_-_$t.flac"/e' *.flac

find . -name "*.flac" -exec metaflac --remove-tag=ARTIST \
	--set-tag=ARTIST="Robbie Williams" \
	--remove-tag=ALBUM \
	--set-tag=ALBUM="In And Out Of Consciousness" {} +

find . -name "*.flac" -exec metaflac --remove-tag=ARTIST \
	--set-tag=ARTIST="Bad Company" \
	--remove-tag=ALBUM \
	--set-tag=ALBUM="Burnin Sky" {} +

metaflac --export-tags-to=- file.flac

rename -n 's{^(\d{2}) - (.+)\.flac$}{ "1_" . $1 . "_-_The_Moody_Blues_-_The_Present_-_" . join("_", map { ucfirst } split(" ", $2)) . ".flac" }e' *.flac






find . -name "*.mp3" -exec eyeD3 \
    --remove-all-lyrics \
    --remove-frame TPUB \
    --remove-frame TXXX \
    --remove-frame COMM \
    --remove-frame TIT1 \
    --remove-frame TPE2 \
    --remove-frame TSRC \
    --remove-frame TYER \
    --remove-frame TMED \
    --remove-frame TDRC \
    --remove-frame TRDA \
    --remove-frame TDAT \
    --remove-frame TDOR \
    --remove-frame TEXT \
    --remove-frame TOLY \
    --remove-frame TCOM \
    --remove-frame TBPM \
    --remove-frame TPE3 \
    --remove-frame TPE4 \
    --remove-frame UFID \
    --remove-frame RGAD {} +
