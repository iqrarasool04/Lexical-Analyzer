#include <iostream>
#include <string>

using namespace std;

int main() {
    string name = "John";
    int age = 25;

    cout << "Name: " << name << endl;
    cout << "Age: " << age << endl;

    if (age >= 18) {
        cout << "You are an adult." << endl;
    } else {
        cout << "You are not an adult." << endl;
    }

    return 0;
}

