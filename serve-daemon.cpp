#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <cstdio>
#include <iomanip>
#include <cstring>

std::string pad(char* serverid, char* msgid) {

    std::stringstream ss;
    ss << "db/" << "server/" << std::setfill('0') << std::setw(16) << std::string(serverid) << "/";
    ss << std::setfill('0') << std::setw(16) << std::string(msgid);
    std::string loc = ss.str();

    return loc;    

}

std::vector<std::string> read(char* serverid, char* msgid) {
    
    std::string loc = pad(serverid, msgid);
    std::ifstream fis;
    std::vector<std::string> out = {};

    fis.open(loc);
    if (!fis.is_open()) {
        std::cerr << "404 not found";
    } else {
        std::string line;
        while (std::getline(fis, line)) {
            std::cout << line << "\n";
        }
    }
    
    return out;

}

int main(int argc, char* argv[]) {

    if (strcmp(argv[1], "read") == 0) {

        char* serverid = argv[2];
        char* msgid = argv[3];
        std::string path = pad(serverid, msgid);

        std::cout << path << std::endl;
        
    } else if (strcmp(argv[1], "write") == 0) {

    }

    return 0;

}