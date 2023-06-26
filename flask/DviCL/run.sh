for dataset in ud-amazon.txt ud-BerkStan.txt ud-Epinion.txt ud-Gnutella.txt ud-Google.txt ud-LiveJournal.txt ud-NotreDame.txt ud-Pokec.txt ud-Slashdot0811.txt ud-Slashdot0902.txt ud-Stanford.txt ud-WikiTalk.txt ud-wikivote.txt ud-Youtube.txt ud-Orkut.txt; do
  echo;
    ./bliss   ~/data/$dataset;
    cp canon.txt temp.txt;
    ./bliss temp.txt;
    diff canon.txt temp.txt;
  echo;
done
for dataset in ud-BuzzNet.txt ud-Delicious.txt ud-Digg.txt ud-Flixster.txt ud-Foursquare.txt ud-Friendster.txt ud-Lastfm.txt; do
  echo;
  ./bliss   ~/Cliquedata/$dataset;
    cp canon.txt temp.txt;
    ./bliss temp.txt;
    diff canon.txt temp.txt;
  echo;
done
