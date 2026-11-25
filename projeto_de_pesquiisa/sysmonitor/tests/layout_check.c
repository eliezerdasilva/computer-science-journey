#include <stddef.h>
#include "sysmonitor.h"
_Static_assert(sizeof(SmProcess) == 80, "SmProcess layout diverged from NASM offsets");
_Static_assert(sizeof(SmSensor) == 104, "SmSensor layout diverged from NASM offsets");
_Static_assert(sizeof(SmStorageInfo) == 120, "SmStorageInfo layout diverged from NASM offsets");
_Static_assert(offsetof(SmLists, processes) == 16, "process array offset mismatch");
_Static_assert(offsetof(SmLists, sensors) == 10256, "sensor array offset mismatch");
_Static_assert(offsetof(SmLists, storage) == 11920, "storage array offset mismatch");
_Static_assert(offsetof(SmCpuInfo, core_usage) == 152, "CPU core array offset mismatch");
int main(void) { return 0; }
