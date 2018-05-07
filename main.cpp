#include <iostream>
#include <string>
#include <regex>
#include <fstream>

int main() {

    std::ifstream input;
    input.open("../GreatGrandmasComplete.txt");
    std::ofstream quotes;
    quotes.open("../quotes.txt");
    std::ofstream book;
    book.open("../book.txt");
    std::ofstream output;
    output.open("../output.txt");

    if (input.is_open()) {
        std::cout << "The file is open" << std::endl;
    }
    else {
        std::cout << "The file is closed" << std::endl;
    }

    while (!input.eof()) {
        std::string s = "";
        std::regex e("^\\++");
        std::regex f("^[A-Z][A-Z][A-Z\\s]+");
        std::cmatch m;
        getline(input, s);
        if (std::regex_search(s.c_str(), m, e)) {
//            for (auto x : m) std::cout << x << " " << std::endl;
            for (auto x : m) quotes << x << std::endl;
            getline(input, s);
            while (!std::regex_search(s.c_str(), m, e)) {
                getline(input, s);
                quotes << s << std::endl;
            }
        }
        else if (std::regex_search(s.c_str(), m, f)) {
            std::cout << "Recipe Title:\t" << s << std::endl;
            std::cout << "[New title or ENTER to continue]:";
            std::string newTitle;
            getline(std::cin, newTitle);
            if (newTitle.empty()) {
                book << s << std::endl;
                output << s << std::endl;
            }
            else {
                book << newTitle << std::endl;
                output << newTitle << std::endl;
            }
        }
        else {
            book << s << std::endl;
        }
    }

    quotes.close();
    book.close();
    output.close();
    return 0;
}