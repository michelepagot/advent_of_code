#include <stdio.h>
#ifdef SOMETHING_WINDOWS
#include <windows.h>
#include <stdint.h> // for uint32_t
#endif

#ifdef SOMETHING_LINUX
#include <stdlib.h>
#include <string.h>
#endif

typedef struct  {
    uint32_t size;
    void *memory;
} debug_read_file_result;

typedef enum {
    E_PARS_NONE,
    E_PARS_COLUMN1,
    E_PARS_COLUMN2,
    E_PARS_SPACE,
    E_PARS_EOL
} Parser_stat;



#ifdef SOMETHING_WINDOWS
int main() {
    char *fileName;
    debug_read_file_result result = {};
    HANDLE file = CreateFileA(TEXT("input"),
                              GENERIC_READ,
                              0,
                              0,
                              OPEN_EXISTING,
                              FILE_ATTRIBUTE_NORMAL,
                              0);

    SIZE_T fileSize;

    if(file == INVALID_HANDLE_VALUE) {
        printf("INVALID_HANDLE_VALUE\n");
        return 1;
    }

    if(!GetFileSizeEx(file, &fileSize)) {
        printf("Error GetFileSizeEx\n");
        return 1;
    }

    LPVOID memory = VirtualAlloc(
                        0,
                        fileSize,
                        MEM_COMMIT | MEM_RESERVE,
                        PAGE_READWRITE);
    if(!memory) {
        printf("Error VirtualAlloc\n");
        return 1;
    }
    DWORD bytesRead;
    if(ReadFile(file, memory, fileSize, &bytesRead, 0)
            && bytesRead == fileSize) {
        result.size = fileSize;
        result.memory = memory;
    } else {
        printf("Error ReadFile\n");
        return 1;
    }

    CloseHandle(file);
    printf("Size:%d\n", result.size);
    unsigned char *p = result.memory;
    Parser_stat stat = E_PARS_NONE;
    int col1[1005];
    int col2[1005];
    int row = 0;
    for(uint32_t idx=0; idx < result.size; idx++) {
        switch(stat) {
        case E_PARS_NONE:
            if((p[idx] >= '0') && (p[idx] <= '9')) {
                stat = E_PARS_COLUMN1;
                col1[row] = strtod(&p[idx], NULL);
                //printf("Col1:%d\n", col1[row]);
            }
            else {
                printf("Unexpected p[%d]=%X in E_PARS_NONE\n", idx, p[idx]);
            }
            break;

        case E_PARS_COLUMN1:
            if(p[idx] == ' ') {
                stat = E_PARS_SPACE;
            }
            else if((p[idx] >= '0') && (p[idx] <= '9')) {
                stat = E_PARS_COLUMN1;
            }
            else {
                printf("Unexpected p[%d]=%X in E_PARS_COLUMN1\n", idx, p[idx]);
                stat = E_PARS_NONE;
            }
            break;

        case E_PARS_SPACE:
            if(p[idx] == ' ') {
                stat = E_PARS_SPACE;
            }
            else if((p[idx] >= '0') && (p[idx] <= '9')) {
                stat = E_PARS_COLUMN2;
                col2[row] = strtod(&p[idx], NULL);
                //printf("Col2:%d\n", col2[row]);
                row++;
            }
            else {
                printf("Unexpected p[%d]=%X in E_PARS_SPACE\n", idx, p[idx]);
                stat = E_PARS_NONE;
            }
            break;

        case E_PARS_COLUMN2:
            if((p[idx] == 10) || (p[idx] == 13)) {
                stat = E_PARS_EOL;
            }
            else if((p[idx] >= '0') && (p[idx] <= '9')) {
                stat = E_PARS_COLUMN2;
            }
            else {
                printf("Unexpected p[%d]=%X in E_PARS_COLUMN2\n", idx, p[idx]);
                stat = E_PARS_NONE;
            }
            break;

        case E_PARS_EOL:
            if((p[idx] == 10) || (p[idx] == 13)) {
                stat = E_PARS_EOL;
            }
            else if((p[idx] >= '0') && (p[idx] <= '9')) {
                stat = E_PARS_COLUMN1;
                col1[row] = strtod(&p[idx], NULL);
                //printf("Col1:%d\n", col1[row]);
            }
            else {
                printf("Unexpected p[%d]=%X in E_PARS_EOL\n", idx, p[idx]);
                stat = E_PARS_NONE;
            }
            break;

        default:
            printf("Unexpected stat:%d at p[%d]=%X\n", stat, idx, p[idx]);
            break;
        };
    }

    int tmp;
    for (int i = 0; i < row; ++i)
    {
        for (int j = i + 1; j < row; ++j)
        {
            if (col1[i] > col1[j])
            {
                tmp =  col1[i];
                col1[i] = col1[j];
                col1[j] = tmp;
            }
            if (col2[i] > col2[j])
            {
                tmp =  col2[i];
                col2[i] = col2[j];
                col2[j] = tmp;
            }
        }
    }
    int tot=0;
    for (int i = 0; i < row; ++i)
    {
        //printf("Col1:%d  Col2:%d\n", col1[i], col2[i]);
        if (col1[i] >= col2[i]) {
            tot += col1[i] - col2[i];
        }
        else {
            tot += col2[i] - col1[i];
        }
    }

    printf("Part1:%d\n\n", tot);
}
#else
int main(int argc, char **argv) {
    FILE *fp = argc == 2 ? fopen(argv[1],"r") : stdin;
    if (!fp) {
        perror("fopen");
        exit(1);
    }

    char buf[2];
    while(fgets(buf,sizeof(buf),fp) != NULL) {
        size_t l = strlen(buf);
        printf("l:%d\n", l);
        if (l <= 1) continue;
        if (buf[l-1] == '\n') {
            buf[l-1] = 0;
            l--;
        }

        int x,y;
        scanf(buf,"%d %d",&x,&y);
        printf("x:%d y:%d\n",x,y);
    }
    if (argc == 2) fclose(fp);
  return 0;
}
#endif
