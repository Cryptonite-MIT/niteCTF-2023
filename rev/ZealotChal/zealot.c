#include <stdio.h>
#include <string.h>
#include <openssl/md5.h>

void printflag()
{
    FILE *file = fopen("flag.txt", "r");
    if (file == NULL)
    {
        printf("\nThe File is not there in the local directory\n");
        return;
    }
    char line[256];
    printf("\nYou Heretics Sure Do Get On My Nerve\n");
    while (fgets(line, sizeof(line), file))
    {
        printf("%s", line);
    }
    fclose(file);
}

void misdirection()
{
    return;
}

void misdirection2()
{
    return;
}

void misdirectio3()
{
    return;
}

void misdirection4()
{
    return;
}

void misdirection5()
{
    return;
}

void misdirection6()
{
    return;
}

void misdirectio7()
{
    return;
}

void misdirection8()
{
    return;
}

int checkpass(char *arr)
{
    if (
        (arr[5] == 0x54) &&
        (arr[6] == 0x46) &&
        (arr[0] == arr[40]) &&
        ((arr[1] ^ 0x1d) == arr[37]) &&
        (arr[3] == arr[18]) &&
        (arr[18] == arr[32]) &&
        (((arr[2] ^ 0x34)) | 0x14 == arr[5]) &&
        ((~arr[8]) + 0x12 == 0xFFFFFFFFFFFFFFAA) &&
        (arr[37] ^ 0x20 == arr[5]) &&
        (arr[21] == 0x74) &&
        (arr[7] + 0x02 == arr[41]) &&
        (arr[8] << 5 == 0xCE0) &&
        (arr[17] == (0x68)) &&
        (arr[9] == arr[10]) &&
        (arr[14] == arr[29]) &&
        (arr[29] == arr[39]) &&
        (arr[12] == 0x5f) &&
        (arr[16] == ((((arr[12] + 0x7a4756b0) | 0x42b1202) & 0x4cbc4a2e) ^ 0x4c2c4251)) &&
        (arr[0] == 0x6e) &&
        ((((arr[31] ^ arr[41]) & 0x8e56) ^ 0xa144) == (arr[14] ^ 0xd289 - 0x3160)) &&
        (arr[23] == ((((arr[12] + 0xca23762c) | 0x4030040) & 0x664a6966) ^ 0x4602601d)) &&
        (arr[2] == 0x74) &&
        (arr[27] == ((((arr[12] - 0xd0252aa0) & 0xc9ba826b) | 0x395d4b28) ^ 0x39dfcb74)) &&
        (arr[31] == ((((arr[12] - 0xc1653aa0) & 0xda1cff3f) | 0x995980) ^ 0x1a99dde0)) &&
        (((((arr[24] ^ 0x66) | 0x2024006c) & 0x400065) == arr[26])) &&
        ((((arr[24] ^ 0x62) | 0x8006c) & 0x65) == arr[33]) &&
        (((((arr[28] << 0x19) ^ 0x60000000) | 0x1fd090eb) & 0x200673) == arr[35]) &&
        (arr[3] == 0x65) &&
        (arr[28] == 0x66) &&
        (arr[6] + 0x22 == arr[17]) &&
        (arr[41] == 0x7d) &&
        ((arr[20]) == (((((arr[1] + arr[3]) & 0x8450) ^ 0x40) | 0x6c))) &&
        (arr[36] == arr[19]) &&
        (arr[19] == arr[6] + 0x1b) &&
        (arr[34] ^ 0x343180 ^ 0x9739378 ^ 0xd72f76b5 ^ 0xcc5dc719 == 0x12351321) &&
        (arr[1] == 0x69) &&
        ((arr[25]) == (((arr[4] & 0x9068) >> 0x3) ^ 0x69)) &&
        (arr[21] ^ arr[37] == 0x0) &&
        ((arr[20] ^ 0x4e | 0x50) == arr[15]) &&
        ((arr[20] ^ 0x4e | 0x50) == arr[30]) &&
        (arr[11] == arr[22] + (0xFFFFFFFFFFFFFFFC)) &&
        (arr[22] == (((arr[9] ^ arr[12]) & 0xb00b) ^ 0x68)) &&
        (arr[30] == arr[15]) &&
        (arr[24] == ((((arr[5] - 0x1b37a000) & 0x959781db) | 0x4a6b0680) ^ 0xceeb06b2)) &&
        (((arr[9]) == (((0xfa99 & 0x2368) | 0xc80a) ^ 0xea65))) &&
        (arr[4] == 0x43) &&
        ((arr[38]) == ((((~arr[13]) & (arr[20])) ^ 0x9) | 0x68)) &&
        ((arr[13] ^ 0xba6 + 0x4c00) == (arr[20] & 0x4696 ^ 0x57c4))

    )
    {
        return 1;
    }

    return 0;
}

void printBanner()
{
    printf("ZZZZZZZZZZZ       EEEEEEEEEEEE      AAAAA       LL               OOOOOOOOO      TTTTTTTTTTTT  \n");
    printf("      ZZ          EE               A     A      LL             OO         OO         TT       \n");
    printf("    ZZ            EEEEEE          AAAAAAAAA     LL             OO         OO         TT       \n");
    printf(" ZZ               EE              A       A     LL             OO         OO         TT       \n");
    printf("ZZZZZZZZZZZ       EEEEEEEEEEEE    A       A     LLLLLLLLLL       OOOOOOOO            TT       \n");
}

int main()
{
    setbuf(stdout, NULL);
    printBanner();
    char input[45];

    printf("\nSpeak Heretic!!\n");

    scanf("%s", input);

    printf("Password entered is %s", input);

    if (checkpass(input) == 1)
    {
        printf("\nEntered Here");
        printflag();
    }
    else
        printf("\nLeave At Once\n");
    return 0;
}
