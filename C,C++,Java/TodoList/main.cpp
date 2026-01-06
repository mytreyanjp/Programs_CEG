#include <gtkmm/application.h>
#include "todo_list_gui.h"

int main(int argc, char* argv[]) {
    auto app = Gtk::Application::create(argc, argv, "org.gtkmm.example");

    ToDoListGUI window;

    return app->run(window);
}
