#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <wayland-client.h>
#include <xdg-shell-client-protocol.h>
#include <xdg-activation-v1-client-protocol.h>

struct wl_display *display;
struct wl_registry *registry;
struct wl_seat *seat;
struct xdg_activation_v1 *activation = NULL;

void registry_global_handler(void *data, struct wl_registry *registry, uint32_t id, const char *interface, uint32_t version) {
    if (strcmp(interface, xdg_activation_v1_interface.name) == 0) {
        activation = wl_registry_bind(registry, id, &xdg_activation_v1_interface, 1);
    } else if (strcmp(interface, wl_seat_interface.name) == 0) {
        seat = wl_registry_bind(registry, id, &wl_seat_interface, 1);
    }
}

void registry_global_remove_handler(void *data, struct wl_registry *registry, uint32_t id) {
    // Handle removal if necessary
}

static void token_done(void *data, struct xdg_activation_token_v1 *xdg_activation_token_v1, const char *token) {
    struct wl_surface *surface = (struct wl_surface *)data;
    if (activation && surface) {
        xdg_activation_v1_activate(activation, token, surface);
    }
    free((void *)token);
}

static const struct xdg_activation_token_v1_listener token_listener = {
    .done = token_done,
};

int main(int argc, char *argv[]) {
    display = wl_display_connect(NULL);
    if (!display) {
        fprintf(stderr, "Failed to connect to the Wayland display\n");
        return EXIT_FAILURE;
    }

    registry = wl_display_get_registry(display);
    wl_registry_add_listener(registry, &(struct wl_registry_listener) {
        .global = registry_global_handler,
        .global_remove = registry_global_remove_handler,
    }, NULL);

    wl_display_roundtrip(display);

    if (!activation) {
        fprintf(stderr, "Compositor does not support xdg_activation_v1\n");
        return EXIT_FAILURE;
    }

    pid_t pid = getpid();  // Replace with the PID of the window you want to activate
    struct wl_surface *surface = NULL;  // Replace with the actual wl_surface of your window

    struct xdg_activation_token_v1 *token = xdg_activation_v1_get_activation_token(activation);
    xdg_activation_token_v1_set_pid(token, pid);
    xdg_activation_token_v1_set_surface(token, surface);
    xdg_activation_token_v1_add_listener(token, &token_listener, surface);
    xdg_activation_token_v1_commit(token);

    wl_display_roundtrip(display);

    wl_display_disconnect(display);

    return EXIT_SUCCESS;
}
