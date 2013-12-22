#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define DEFAULT_BYTES_TO_SPLIT_LINES 256;

static char * prog;
// strdupしなくてもよいのか・・・？

void usage() {
    fprintf(stderr, "Usage: %s [-s slice] [-A start] [-B end] <filename|->\n", prog);
}

int main(int argc, char *argv[]){
    prog = argv[0];
    int fd;
    int ch;
    extern char * optarg;
    extern int optind, opterr;

    unsigned long slice_bytes = DEFAULT_BYTES_TO_SPLIT_LINES;
    unsigned long start_bytes = 0;
    unsigned long end_bytes = 0;
    while ( (ch = getopt(argc,argv,"A:B:s:") ) != -1) {
    switch (ch) {
        case 's':
            slice_bytes = (unsigned long)atol(optarg);
            if (slice_bytes == 0)
                slice_bytes = DEFAULT_BYTES_TO_SPLIT_LINES;
            break;
        case 'A':
            start_bytes = (unsigned long)atol(optarg);
            break;
        case 'B':
            end_bytes = (unsigned long)atol(optarg);
            break;
        case '?':
        default:
            usage();
            return -1;
    }
    }
    argc -= optind;
    argv += optind;
    if ( argc != 1 ) {
        usage();
        return 1;
    }
    if (argv[0][0] == '-')
        fd = 0;//stdin
    else
        fd = open(argv[0], O_RDONLY);
    if ( fd < 0 ) {
        fprintf(stderr, "Can't read file %s\n", argv[0]);
        return 1;
    }
    if (start_bytes > 0) {
        char buf[start_bytes];
        read(fd, buf, start_bytes);
        end_bytes = end_bytes - start_bytes;
    }
    unsigned long i = 0;
    do {
        unsigned char buf;
        int read_size;
        read_size = read(fd, &buf, 1);
        if ( read_size > 0 ){
            ++i;
            unsigned char ch='.';
            if (buf > 0x20 & buf < 0x7F)
                ch=buf;
            if (buf == '0')//WHITE
                printf("\x1b[47m");
            else if (buf < 32)//CYAN
                printf("\x1b[46m");
            else if (buf < 128)//RED
                printf("\x1b[41m");
            else//BLACK
                printf("\x1b[48;5;16m")//printf("\x1b[40m")
            putchar(ch);
            printf("\x1b[0m");
            //fflush(stdout);
        } else if ( read_size == 0 ){
            break;
        } else {
            fprintf(stderr, "\nCan't continue reading file %s\n", argv[0]);
            return 1;
        }
        if (i % slice_bytes == 0)
            puts("");
    } while (end_bytes - i > 0);
    close(fd);
    puts("");
    return 0;
}
