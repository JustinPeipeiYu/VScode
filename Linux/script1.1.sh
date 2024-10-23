#! /bin/bash
mkdir justin
cp nursery justin/; cp sonnet justin/
cd justin
mkdir files1
mkdir files1/sonnets
mkdir files1/rhymes
mkdir files1/combos
cat nursery sonnet > poems
mv sonnet files1/sonnets
mv nursery files1/rhymes
mv poems files1/combos
cd ../../../..
cd home
cd yu
cp -r labfiles/justin labfiles/ahmed
cd labfiles/justin
cp -r files1 files2
cd files1/sonnets
cp sonnet bonnet
cp sonnet donnet
