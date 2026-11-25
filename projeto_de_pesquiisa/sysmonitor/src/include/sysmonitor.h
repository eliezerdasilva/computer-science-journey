#ifndef SYSMONITOR_H
#define SYSMONITOR_H
#include <stdint.h>
#define SM_MAX_CORES 64
#define SM_MAX_PROCESSES 128
#define SM_MAX_SENSORS 16
#define SM_NAME_LEN 64
#define SM_LABEL_LEN 96

typedef struct { char model[128]; uint64_t logical_count, usage_percent, core_count; uint64_t core_usage[SM_MAX_CORES]; } SmCpuInfo;
typedef struct { uint64_t total_kb, available_kb, used_kb, swap_total_kb, swap_free_kb; } SmMemoryInfo;
typedef struct { uint64_t uptime_seconds; } SmUptimeInfo;
typedef struct { uint64_t rx_bytes, tx_bytes, rx_delta_bytes, tx_delta_bytes; } SmNetworkInfo;
typedef struct { uint32_t pid; char name[SM_NAME_LEN]; char state; uint64_t rss_kb; } SmProcess;
typedef struct { uint64_t total_bytes, available_bytes, used_bytes; char mountpoint[SM_LABEL_LEN]; } SmStorageInfo;
typedef struct { char label[SM_LABEL_LEN]; int64_t milli_celsius; } SmSensor;
typedef struct { uint32_t process_count, sensor_count, storage_count, reserved; SmProcess processes[SM_MAX_PROCESSES]; SmSensor sensors[SM_MAX_SENSORS]; SmStorageInfo storage[8]; } SmLists;

int64_t sm_read_cpu(SmCpuInfo *out);
int64_t sm_read_memory(SmMemoryInfo *out);
int64_t sm_read_uptime(SmUptimeInfo *out);
int64_t sm_read_network(SmNetworkInfo *out);
int64_t sm_read_processes(SmLists *out);
int64_t sm_read_storage(SmLists *out);
int64_t sm_read_sensors(SmLists *out);
int64_t sm_send_signal(uint32_t pid, int signal_number);
#endif
