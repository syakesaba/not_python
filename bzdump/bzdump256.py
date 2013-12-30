#!/usr/bin/env python
# encoding: utf-8

import sys
import atexit
import argparse #Use Python(>=2.7)

S_WHITE = "\x1b[47m"
S_CYAN = "\x1b[46m"
S_RED = "\x1b[41m"
S_BLACK = "\x1b[48;5;16m" #"\x1b[40m"
E_SEQ = "\x1b[0m"

parser = argparse.ArgumentParser(description="BzEditor-like binary bitmapper in CUI")
parser.add_argument("file", type=argparse.FileType("r"), nargs='?',
                    help="File to read. (if null or \"-\", read from stdin)",
                    default=sys.stdin)
parser.add_argument("-s", "--slice", metavar="N", type=int,default=0,
                    help="N Bytes to slice with \\n. (default 0)")
parser.add_argument("-A", "--begin", metavar="N", type=int,default=0,
                    help="First N Bytes to begin. (default 0)")
parser.add_argument("-B", "--end", metavar="N", type=int,default=None,
                    help="Last(or least) N Bytes to end."
                        +"A negative value is allowed. (e.g. -120 )")
parser.add_argument("-S", "--split", metavar="N", type=int, default=1,
                    help="split each N Bytes. (default 1)")
parser.add_argument("-v", "--verbose", action="count", default=0,
                    help="verbose mode (not implemented)")
parser.add_argument("-c", "--char", action="store_true",
                    help="print ascii char mode")
parser.add_argument("-d", "--debug", action="store_true",
                    help="debug mode (opening Python interactive shell)")
results = parser.parse_args()
if results.verbose:
    print >> sys.stderr, "opened %s" % results.file.name
def close_file(result):
    if not result.file.closed:
        if result.verbose:
            print >> sys.stderr, "closing %s" % result.file.name
        result.file.close()
atexit.register(close_file, results)
buf = results.file.read()
target = buf[results.begin:results.end:results.split]
p = sys.stdout.write
for i,c in enumerate(target):
    ch = ord(c)
    if ch == 0:
        p(S_WHITE)
    elif ch < 32:
        p(S_CYAN)
    elif ch < 64:
        p(S_RED)
    else:
        p(S_BLACK)
    if results.char:
        p(ch > 0x1F and ch < 0x7F and c or ".")
    else:
        p(" ")
    p(E_SEQ)
    if results.slice != 0 and (i + 1) % results.slice == 0:
        print
print
if results.debug:
    try:
        import rlcompleter
        rlcompleter.readline.parse_and_bind("tab: complete")
        rlcompleter.readline.set_history_length(1000)
        sys.ps1 ="\x1B[1m\x1B[31m>\x1B[33m>\x1B[32m>\x1B[0m "
    except:
        pass
    import code
    code.interact(banner="Debug Mode! check results.file!",local=locals())
# TODO: 行番号をverboseによって表示, fileコマンド連携(stdinパイプ、ret値使用)
