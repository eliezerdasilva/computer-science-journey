#include <gtk/gtk.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include "sysmonitor.h"

static SmCpuInfo cpu_data;
static SmMemoryInfo mem_data;
static SmUptimeInfo uptime_data;
static SmNetworkInfo net_data;
static SmLists lists;
static GtkWidget *cpu_label, *mem_label, *uptime_label, *network_label;
static GtkWidget *process_view, *sensor_label, *storage_label, *status_label;
static GtkWidget *window;

static char *format_bytes(uint64_t bytes) {
    const char *units[] = {"B", "KiB", "MiB", "GiB", "TiB"};
    double value = (double)bytes;
    unsigned i = 0;
    while (value >= 1024.0 && i < 4) { value /= 1024.0; i++; }
    return g_strdup_printf("%.1f %s", value, units[i]);
}

static void refresh_processes(void) {
    GtkTextBuffer *buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(process_view));
    GtkTextIter end;
    gtk_text_buffer_set_text(buffer, "PID       ESTADO  RSS       NOME\n", -1);
    gtk_text_buffer_get_end_iter(buffer, &end);
    for (uint32_t i = 0; i < lists.process_count && i < SM_MAX_PROCESSES; i++) {
        SmProcess *p = &lists.processes[i];
        char *line = g_strdup_printf("%-9u %-7c %-9" G_GUINT64_FORMAT " %s\n", p->pid, p->state, p->rss_kb, p->name);
        gtk_text_buffer_insert(buffer, &end, line, -1);
        g_free(line);
    }
}

static gboolean refresh_data(gpointer unused) {
    (void)unused;
    int cpu_rc = sm_read_cpu(&cpu_data);
    int mem_rc = sm_read_memory(&mem_data);
    int up_rc = sm_read_uptime(&uptime_data);
    int net_rc = sm_read_network(&net_data);
    sm_read_processes(&lists);
    sm_read_storage(&lists);
    sm_read_sensors(&lists);

    if (cpu_rc == 0) {
        GString *cpu_text = g_string_new(NULL);
        g_string_append_printf(cpu_text,
            "Modelo: %s\nProcessadores lógicos: %" G_GUINT64_FORMAT "\nUso agregado: %" G_GUINT64_FORMAT "%%",
            cpu_data.model[0] ? cpu_data.model : "Não identificado", cpu_data.logical_count, cpu_data.usage_percent);
        for (uint64_t i = 0; i < cpu_data.core_count && i < SM_MAX_CORES; i++) {
            g_string_append_printf(cpu_text, "\nCPU%-2" G_GUINT64_FORMAT ": %" G_GUINT64_FORMAT "%%", i, cpu_data.core_usage[i]);
        }
        gtk_label_set_text(GTK_LABEL(cpu_label), cpu_text->str);
        g_string_free(cpu_text, TRUE);
    }
    if (mem_rc == 0) {
        char *total = format_bytes(mem_data.total_kb * 1024), *used = format_bytes(mem_data.used_kb * 1024);
        char *avail = format_bytes(mem_data.available_kb * 1024);
        char *swap = format_bytes(mem_data.swap_total_kb * 1024), *swapfree = format_bytes(mem_data.swap_free_kb * 1024);
        char *s = g_strdup_printf("RAM total: %s\nRAM em uso: %s\nRAM disponível: %s\nSWAP total: %s\nSWAP livre: %s",
                                  total, used, avail, swap, swapfree);
        gtk_label_set_text(GTK_LABEL(mem_label), s);
        g_free(total); g_free(used); g_free(avail); g_free(swap); g_free(swapfree); g_free(s);
    }
    if (up_rc == 0) {
        uint64_t t = uptime_data.uptime_seconds;
        char *s = g_strdup_printf("%" G_GUINT64_FORMAT " dias, %" G_GUINT64_FORMAT " horas, %" G_GUINT64_FORMAT " minutos, %" G_GUINT64_FORMAT " segundos",
            t / 86400, (t % 86400) / 3600, (t % 3600) / 60, t % 60);
        gtk_label_set_text(GTK_LABEL(uptime_label), s); g_free(s);
    }
    if (net_rc == 0) {
        char *rx = format_bytes(net_data.rx_bytes), *tx = format_bytes(net_data.tx_bytes);
        char *rxs = format_bytes(net_data.rx_delta_bytes), *txs = format_bytes(net_data.tx_delta_bytes);
        char *s = g_strdup_printf("Recebido: %s (delta/amostra: %s)\nTransmitido: %s (delta/amostra: %s)", rx, rxs, tx, txs);
        gtk_label_set_text(GTK_LABEL(network_label), s);
        g_free(rx); g_free(tx); g_free(rxs); g_free(txs); g_free(s);
    }
    refresh_processes();
    if (lists.sensor_count) {
        SmSensor *sensor = &lists.sensors[0];
        char *sensor_text = g_strdup_printf("%s: %.1f °C", sensor->label, sensor->milli_celsius / 1000.0);
        gtk_label_set_text(GTK_LABEL(sensor_label), sensor_text);
        g_free(sensor_text);
    } else gtk_label_set_text(GTK_LABEL(sensor_label), "Sensores térmicos não disponíveis neste equipamento.");
    if (lists.storage_count) {
        SmStorageInfo *st = &lists.storage[0];
        char *total = format_bytes(st->total_bytes), *used = format_bytes(st->used_bytes), *avail = format_bytes(st->available_bytes);
        char *s = g_strdup_printf("Partição raiz (/): %s total | %s usado | %s disponível", total, used, avail);
        gtk_label_set_text(GTK_LABEL(storage_label), s);
        g_free(total); g_free(used); g_free(avail); g_free(s);
    }
    gtk_label_set_text(GTK_LABEL(status_label), "Atualização automática a cada 1 segundo. Alguns sensores dependem do suporte do kernel/hardware.");
    return G_SOURCE_CONTINUE;
}

static void on_refresh(GtkButton *button, gpointer data) { (void)button; (void)data; refresh_data(NULL); }
static void on_close(GtkButton *button, gpointer data) { (void)button; (void)data; gtk_window_close(GTK_WINDOW(window)); }

static GtkWidget *section(const char *title, GtkWidget *content) {
    GtkWidget *frame = gtk_frame_new(title);
    gtk_frame_set_child(GTK_FRAME(frame), content);
    gtk_widget_set_margin_top(frame, 6); gtk_widget_set_margin_bottom(frame, 6);
    return frame;
}

static void activate(GtkApplication *app, gpointer user_data) {
    (void)user_data;
    window = gtk_application_window_new(app);
    gtk_window_set_title(GTK_WINDOW(window), "SysMonitor — Monitor do sistema Linux");
    gtk_window_set_default_size(GTK_WINDOW(window), 980, 720);
    GtkWidget *root = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    gtk_widget_set_margin_start(root, 16); gtk_widget_set_margin_end(root, 16);
    gtk_widget_set_margin_top(root, 16); gtk_widget_set_margin_bottom(root, 12);
    gtk_window_set_child(GTK_WINDOW(window), root);
    GtkWidget *heading = gtk_label_new(NULL);
    gtk_label_set_markup(GTK_LABEL(heading), "<span size='xx-large' weight='bold'>SYSMONITOR</span>  <span alpha='70%'>Linux x86-64 • NASM + GTK 4</span>");
    gtk_box_append(GTK_BOX(root), heading);
    GtkWidget *grid = gtk_grid_new();
    gtk_grid_set_row_spacing(GTK_GRID(grid), 8); gtk_grid_set_column_spacing(GTK_GRID(grid), 8);
    gtk_widget_set_vexpand(grid, TRUE);
    cpu_label = gtk_label_new("Coletando dados..."); gtk_label_set_xalign(GTK_LABEL(cpu_label), 0);
    mem_label = gtk_label_new("Coletando dados..."); gtk_label_set_xalign(GTK_LABEL(mem_label), 0);
    uptime_label = gtk_label_new("Coletando dados..."); gtk_label_set_xalign(GTK_LABEL(uptime_label), 0);
    network_label = gtk_label_new("Coletando dados..."); gtk_label_set_xalign(GTK_LABEL(network_label), 0);
    sensor_label = gtk_label_new("Consultando sensores..."); gtk_label_set_xalign(GTK_LABEL(sensor_label), 0);
    storage_label = gtk_label_new("Consultando armazenamento..."); gtk_label_set_xalign(GTK_LABEL(storage_label), 0);
    gtk_grid_attach(GTK_GRID(grid), section("CPU", cpu_label), 0, 0, 1, 1);
    gtk_grid_attach(GTK_GRID(grid), section("Memória RAM e SWAP", mem_label), 1, 0, 1, 1);
    gtk_grid_attach(GTK_GRID(grid), section("Tempo de atividade", uptime_label), 0, 1, 1, 1);
    gtk_grid_attach(GTK_GRID(grid), section("Rede", network_label), 1, 1, 1, 1);
    gtk_grid_attach(GTK_GRID(grid), section("Armazenamento", storage_label), 0, 2, 1, 1);
    gtk_grid_attach(GTK_GRID(grid), section("Temperatura", sensor_label), 1, 2, 1, 1);
    gtk_box_append(GTK_BOX(root), grid);
    process_view = gtk_text_view_new();
    gtk_text_view_set_editable(GTK_TEXT_VIEW(process_view), FALSE);
    gtk_text_view_set_monospace(GTK_TEXT_VIEW(process_view), TRUE);
    gtk_widget_set_size_request(process_view, -1, 180);
    GtkWidget *scroll = gtk_scrolled_window_new();
    gtk_scrolled_window_set_child(GTK_SCROLLED_WINDOW(scroll), process_view);
    gtk_box_append(GTK_BOX(root), section("Processos (PID, estado, RSS e nome)", scroll));
    GtkWidget *actions = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 8);
    GtkWidget *refresh = gtk_button_new_with_label("Atualizar agora");
    GtkWidget *close = gtk_button_new_with_label("Fechar");
    g_signal_connect(refresh, "clicked", G_CALLBACK(on_refresh), NULL);
    g_signal_connect(close, "clicked", G_CALLBACK(on_close), NULL);
    gtk_box_append(GTK_BOX(actions), refresh); gtk_box_append(GTK_BOX(actions), close);
    gtk_box_append(GTK_BOX(root), actions);
    status_label = gtk_label_new(""); gtk_label_set_xalign(GTK_LABEL(status_label), 0);
    gtk_box_append(GTK_BOX(root), status_label);
    refresh_data(NULL);
    g_timeout_add_seconds(1, refresh_data, NULL);
    gtk_window_present(GTK_WINDOW(window));
}

int main(int argc, char **argv) {
    GtkApplication *app = gtk_application_new("br.edu.sysmonitor", G_APPLICATION_DEFAULT_FLAGS);
    g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);
    int status = g_application_run(G_APPLICATION(app), argc, argv);
    g_object_unref(app);
    return status;
}
