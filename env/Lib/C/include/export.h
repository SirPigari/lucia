#ifndef EXPORT_H
#define EXPORT_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#ifndef EXPORT_FILE_PATH
#define EXPORT_FILE_PATH "export.json"
#endif
#ifndef AUTO_FLUSH
#define AUTO_FLUSH false
#endif

typedef struct ExportEntry {
    char* key;
    char* value;
    struct ExportEntry* next;
} ExportEntry;

static ExportEntry* export_head = NULL;

static inline void export_flush(void);

static void export_add(const char* name, const char* raw_value) {
    ExportEntry* entry = malloc(sizeof(ExportEntry));
    entry->key = strdup(name);
    entry->value = strdup(raw_value);
    entry->next = export_head;
    export_head = entry;
    if (AUTO_FLUSH) {
        export_flush();
    }
}

static char* json_escape_string(const char* input) {
    size_t len = strlen(input);
    char* escaped = malloc(len * 2 + 3);
    char* dst = escaped;
    *dst++ = '"';
    for (const char* src = input; *src; ++src) {
        if (*src == '"' || *src == '\\') {
            *dst++ = '\\';
        }
        *dst++ = *src;
    }
    *dst++ = '"';
    *dst = '\0';
    return escaped;
}

static inline void export_string(const char* name, const char* value) {
    char* escaped = json_escape_string(value);
    export_add(name, escaped);
    free(escaped);
}

static inline void export_int(const char* name, int value) {
    char buffer[32];
    sprintf(buffer, "%d", value);
    export_add(name, buffer);
}

static inline void export_float(const char* name, float value) {
    char buffer[32];
    sprintf(buffer, "%f", value);
    export_add(name, buffer);
}

static inline void export_double(const char* name, double value) {
    char buffer[64];
    sprintf(buffer, "%.17g", value);
    export_add(name, buffer);
}

static inline void export_bool(const char* name, int value) {
    export_add(name, value ? "true" : "false");
}

static inline void export_flush() {
    FILE* f = fopen(EXPORT_FILE_PATH, "w");
    if (!f) return;

    fprintf(f, "{");
    ExportEntry* current = export_head;
    while (current) {
        fprintf(f, "\"%s\": %s", current->key, current->value);
        if (current->next) fprintf(f, ", ");
        current = current->next;
    }
    fprintf(f, "}\n");

    fclose(f);
}

static inline void export_clear() {
    ExportEntry* current = export_head;
    while (current) {
        ExportEntry* next = current->next;
        free(current->key);
        free(current->value);
        free(current);
        current = next;
    }
    export_head = NULL;
}

#endif
