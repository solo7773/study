# no shebang line

import sys
import os

if len(sys.argv) != 2:
  sys.exit('Please give the GTF filename in the command line.\n')
gtfName = sys.argv[1]

lineAbove = None
INGTF = open(gtfName, 'r')
OUT5SSREGION = open(gtfName + '.5ssRegion.bed', 'w')
#OUT5SSREGION.write("Pre exon\tNext exon\t5ssStart\t5ssEnd\tstrand\n")
for thisLine in INGTF:
  thisLine = thisLine.strip()
  if thisLine[0] == '#':
    continue
  if thisLine.split('\t')[2] == 'transcript':
    #OUT5SSREGION.write(str(str(lineAbove).split('\t')[3:5]) + '\t' + str(thisLine.split('\t')[3:5]) + "\tLast exon no 5 ss\n")
    lineAbove = None
    thisLine = None
    continue
  if not thisLine.split('\t')[2] == 'exon':
    continue
  # exon in this line, parsing
  if lineAbove is None:
    lineAbove = thisLine
    continue
  else:
    exonAbove = [int(x) for x in lineAbove.split('\t')[3:5]]
    exonThis = [int(x) for x in thisLine.split('\t')[3:5]]
    #OUT5SSREGION.write(str(exonAbove) + '\t' + str(exonThis) + '\t')
    if exonAbove[1] < exonThis[0]:
      ssStart = exonAbove[0] if exonAbove[1] - 200 < exonAbove[0] else exonAbove[1] - 200
      #ssStart = exonAbove[1] - 1
      ssEnd = exonThis[0] if exonAbove[1] + 200 > exonThis[0] else exonAbove[1] + 200
      #ssEnd = exonAbove[1] + 1
      OUT5SSREGION.write(lineAbove.split('\t')[0] + '\t' + str(ssStart) + '\t' + str(ssEnd) + '\t' + str(exonAbove[1]) + '\n')
    else:
      continue
      ssStart = exonThis[0] if exonThis[1] - 200 < exonThis[0] else exonThis[1] - 200
      ssEnd = exonAbove[0] if exonThis[1] + 200 > exonAbove[0] else exonThis[1] + 200
      OUT5SSREGION.write(lineAbove.split('\t')[0] + '\t' + str(ssStart) + '\t' + str(ssEnd) + '\t' + str(exonThis[1]) + "\n")
    lineAbove = thisLine

INGTF.close()
OUT5SSREGION.close()

print("Done!")
