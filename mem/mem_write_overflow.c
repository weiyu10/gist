#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define SIZE    10
void dump_mem(char *ptr, int bytes)
{
    int i;
    printf("dump memory for %p \n", ptr);
    for (i = 0; i < bytes; i++) {
            printf("%0x ", *(ptr + i));
            if (((i + 1) % 8) == 0) {
               printf("\n");
	    }
    }
    printf("\n");
}

int main()
{
        char *word = "http://10.10.100.10:9999"; // 字符串长度是24
        char *addrs[SIZE];
        char *chunk;

        // 连续申请两块内存，但是程序有bug，每次都少申请了两个字节
        addrs[0] = malloc(strlen(word+1));
        printf("addrs[0] memory address is %p \n", addrs[0]);
        addrs[1] = malloc(strlen(word+1));
        printf("addrs[1] memory address is %p \n", addrs[1]);

        // 看下当前的内存实际数据
        printf("before release addrs[1]\n");
        dump_mem(addrs[0]-8, 50);

        // 释放第二个chunk 并观察内存信息
        free(addrs[1]);
        printf("after release addrs[1]\n");
        dump_mem(addrs[0]-8, 50);

        // 执行一次会有内存越界的内存拷贝,预期这次越界会写到第二个chunk元数据
        strcpy(addrs[0], word);
        printf("after write overflow on addrs[0]\n");

        // 这次应该能够看到第二个chunk的元数据被覆盖掉了
        dump_mem(addrs[0]-8, 50);

        // 再次申请内存，会尝试使用chunk2
        addrs[2] = malloc(strlen(word+1));
}
