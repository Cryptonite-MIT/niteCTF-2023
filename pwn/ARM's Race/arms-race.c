#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
volatile int user = 0;
volatile int length = 0;

char scratch[1000];
int copy_length = 0;
long long int totTime2 = 0;
long long int totTime = 0;
struct timeval tv_u;
struct timeval tv2_u;
void userThread(void* p){
    struct {
    int self_length;
    int self_user;
    char buf[16];
    } locals;
	while (1){
        user = 0;
        length = 16;

        int iter = 0;
        printf("Iterations: ");
        scanf("%d",&iter);
        fflush(stdin);
        int c;
        do{
            c = getchar();
        }while(c != EOF && c != '\n');

        if (iter == -1){
            return;
        }
        printf("Copy Length: ");
        scanf("%d",&copy_length);
        fflush(stdin);
        do{
            c = getchar();
        }while(c != EOF && c != '\n');

        printf("Enter text to copy:");
        fgets(scratch,1000,stdin);
        fflush(stdin);
        totTime2 = 0;
        totTime = 0;
        iter = iter >= 10000000? 10000000: iter;
        while (iter >= 0)
        {
            locals.self_user = user;
            if (locals.self_user == 0)
            {
                locals.self_length = length;

                gettimeofday( &tv_u, NULL );
               // printf("Iteration: %d, User: %d, Length: %d\n",iter, user, self_length);
                if (locals.self_length > 16)
                {
                   strlen(scratch);
                }

                memcpy(locals.buf,scratch,copy_length >= locals.self_length? locals.self_length: copy_length);
                gettimeofday( &tv2_u, NULL );
                totTime += (tv2_u.tv_sec * 1000000 +  tv2_u.tv_usec) - (tv_u.tv_sec * 1000000 +  tv_u.tv_usec);
                iter--;
                length = 1000;
                user = 1;

            }
        }
        printf("* Thread 1 - 16 character trimmed string: %s\n", locals.buf);
        printf(" | Thread 1 benchmark time: %lldms\n",totTime/1000);
        printf("* Thread 2 - 1000 character trimmed string: %s\n", scratch);
        printf(" | Thread 2 benchmark time: %lldms\n",totTime2/1000);
	}
}

void superThread(void* p){
	char superbuf[1000];
    struct timeval tv,tv2;
	while (1){
        int self_user = user;
		if (self_user == 1){
            int self_length = length;

            //printf("Super response!");
            gettimeofday( &tv, NULL );
            long long int start = tv.tv_sec * 1000000 +  tv.tv_usec;

            memcpy(superbuf, scratch, self_length);

            gettimeofday( &tv2, NULL );
            long long int finish = tv2.tv_sec * 1000000 + tv2.tv_usec;
            totTime2 += (finish-start);
            user = 0;
			length = 16;
		}
	}
}

/*
int stick_this_thread_to_core(pthread_t p, int core_id) {
   int num_cores = sysconf(_SC_NPROCESSORS_ONLN);
   if (core_id < 0 || core_id >= num_cores)
      return -1;

   cpu_set_t cpuset;
   CPU_ZERO(&cpuset);
   CPU_SET(core_id, &cpuset);
   return pthread_setaffinity_np(p, sizeof(cpu_set_t), &cpuset);
}

*/
int main(){
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    printf("---- memcpy Benchmark tool ----\n");
    printf("Super accurate empirical analysis of time complexity!!!\n");
	user = 0;
	length = 16;
	pthread_t thread1, thread2;
    //stick_this_thread_to_core(pthread_self(),0);

    int iret2 = pthread_create( &thread2, NULL, superThread, NULL);
    //stick_this_thread_to_core(thread2,1);

    if (getpid() == gettid()){
        userThread(NULL);
    }
}
