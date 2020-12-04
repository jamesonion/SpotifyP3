#include "Tree.h"
#include <iostream>
#include <unordered_map>
#include <fstream>
#include <string>
#include <set>
#include <algorithm>
#include <map>
#include <fstream>
#include <string>


using namespace std;

//test
//could edit data set to only include the columns we are using to make it faster
void MakeTree(ifstream &file, Tree &valenceTree, Tree &danceTree, Tree &energyTree, Tree &acousticnessTree, unordered_map<string, vector<float>> &IDs, unordered_map<string, pair<string, string>>& songNames) {
    if (file.is_open()) {
        string endLine;
        getline(file, endLine); // get rid of header line
        float valence; // 1st column
        float energy; // 3rd column
        float danceability; // 2nd column
        float acousticness; // 5th column
        float instrumentalness; //6th column
        float speechiness; //7th column
        string temp;
        string ID; // 4th column
        string name; // 8th column
        string artist; // 9th column
        while (!file.eof()) {
            getline(file, temp, ',');

            try {
                valence = stof(temp);
            }
            catch (const invalid_argument &e) {
                break;
            }

            getline(file, temp, ',');
            danceability = stof(temp);
            getline(file, temp, ',');
            energy = stof(temp);
            getline(file, ID, ',');
            getline(file, temp, ',');
            acousticness = stof(temp);
            getline(file, temp, ',');
            instrumentalness = stof(temp);
            getline(file, temp, ',');
            speechiness = stof(temp);

            getline(file, name, ','); // if the name has a comma in it there is a bug
            getline(file, artist); //use until API
            artist.erase(std::remove(artist.begin(), artist.end(), '\''), artist.end());
            artist.erase(std::remove(artist.begin(), artist.end(), '['), artist.end());
            artist.erase(std::remove(artist.begin(), artist.end(), ']'), artist.end());
            artist.erase(std::remove(artist.begin(), artist.end(), '"'), artist.end());


            valenceTree.insert(ID, valence);
            danceTree.insert(ID, danceability);
            energyTree.insert(ID, energy);
            acousticnessTree.insert(ID, acousticness);
            IDs[ID].push_back(valence);
            IDs[ID].push_back(danceability);
            IDs[ID].push_back(energy);
            IDs[ID].push_back(acousticness);
            IDs[ID].push_back(instrumentalness);
            IDs[ID].push_back(speechiness);
            songNames[ID] = make_pair(name, artist);

        }
    }
}

//TODO: CREATE MAP BETWEEN ARTIST AND GENRE
void mapArtistandGenre(ifstream& file, unordered_map<string, vector<string>>& map) {
    string genre, artist, header;
    getline(file, header);
    while (!file.eof()) {
        getline(file, artist, ',');
        artist.erase(std::remove(artist.begin(), artist.end(), '\''), artist.end());
        artist.erase(std::remove(artist.begin(), artist.end(), '['), artist.end());
        artist.erase(std::remove(artist.begin(), artist.end(), ']'), artist.end());
        artist.erase(std::remove(artist.begin(), artist.end(), '"'), artist.end());
        getline(file, genre);
        genre.erase(std::remove(genre.begin(), genre.end(), '"'), genre.end());
        genre.erase(std::remove(genre.begin(), genre.end(), '['), genre.end());
        genre.erase(std::remove(genre.begin(), genre.end(), ']'), genre.end());



        //get rid of all of the ','s in genres
        if (genre.find(',') == string::npos)
            map[artist].push_back(genre);
        else {
            while(genre.find(',') != string::npos) {
                string temp = genre.substr(0, genre.find(','));
                map[artist].push_back(temp);
                genre = genre.substr(genre.find(',') + 1);
            }
            //loop stops before adding the last genre
            string temp = genre.substr(0, genre.find(','));
            map[artist].push_back(temp);
        }
    }
}

void instrumentalAndSpeechCheck(set<string>& suggestable, unordered_map<string, vector<float>>& IDs, float& avgInstrumentalness, float& avgSpeechiness) {
    auto iter = suggestable.begin();
    while (iter != suggestable.end()) {
        if (IDs[*iter][4] > avgInstrumentalness + .25f || IDs[*iter][4] < avgInstrumentalness - .25f) {
            string temp = *iter;
            iter++;
            suggestable.erase(temp);
        }
        else if (IDs[*iter][5] > avgSpeechiness + .2f || IDs[*iter][5] < avgSpeechiness - .2f) {
            string temp = *iter;
            iter++;
            suggestable.erase(temp);
        }
        else {
            iter++;
        }
    }
}

void genreCrossCheck(set<string>& suggestable, unordered_map<string, pair <string, string>>& songNames, unordered_map<string, vector<string>>& artistGenre, set<string>& userLikedGenres) {
    auto iter = suggestable.begin();
    while (iter != suggestable.end()) {
        bool remove = true;
        //Separate songNames.iter.second into separate strings for all the artists
        string artist = songNames[*iter].second;
        while (artist.find(',') != string::npos && remove) {
            string temp = artist.substr(0, artist.find(','));
            for (string x : artistGenre[temp]) {
                if (userLikedGenres.find(x) != userLikedGenres.end()) {
                    remove = false;
                    break;
                }
            }
            artist = artist.substr(artist.find(',') + 2); //substring the actual string to the next artist, + 2 to get past the ", "
        }
        artist = artist.substr(0, artist.find(','));
        if (remove) { //can remove but should lead to some small optimizations
            for (string x : artistGenre[artist]) {
                if (userLikedGenres.find(x) != userLikedGenres.end()) {
                    remove = false;
                    break;
                }
            }
        }
        if (remove) {
            string temp = *iter;
            iter++;
            suggestable.erase(temp);
        }
        else
            iter++;
    }
}
//recursive function to fill set
void songSuggestionSetRec(Tree::Node* curr, set<string>& suggested, float upper, float lower) {
    if (curr == nullptr) {
        return;
    }
    else {
        //if value is inside of range and the node isn't null insert the ID into the set then call function again
        if (curr->left != nullptr && curr->left->value <= upper && curr->left->value >= lower) {
            for (string& x : curr->left->ID)
            suggested.insert(x);
            songSuggestionSetRec(curr->left, suggested, upper, lower);
        }
        if (curr->right != nullptr && curr->right->value <= upper && curr->right->value >= lower) {
            for (string&x : curr->right->ID)
            suggested.insert(x);
            songSuggestionSetRec(curr->right, suggested, upper, lower);
        }
    }
}
//creates set for the given value paramter
//sets will contain the ID's of songs
//this function is somewhat inconcsistent might need to be changed in some ways like finding where to start
set<string> songSuggestionSet(Tree& tree, float value, float range) {
    //traverse the tree
    //new set is created to contain the similar values
    set<string> suggested;
    //the range for the values to be added to the set is from lowerLimit to upperLimit
    float lowerLimit = value - range;
    if (lowerLimit < 0)
        lowerLimit = 0;
    float upperLimit = value + range;
    if (upperLimit > 1)
        upperLimit = 1;
    Tree::Node* temp = tree.root;
    //finds the highest element in the tree that is within the range
    if (value < tree.root->value) {
        while (temp->value > upperLimit)
            temp = temp->left;
    }
    else {
        while (temp->value < lowerLimit)
            temp = temp->right;
    }
    //inserts the first ID into the set then calls the recursive function to add the rest of the values
    for (string&x : temp->ID)
        suggested.insert(x);
    songSuggestionSetRec(temp, suggested, upperLimit, lowerLimit);
    //returns the new set of similar values
    return suggested;
}

set<string> intersection(set<string>& s1, set<string>& s2) {
    set<string> intersect;
    set_intersection(s1.begin(), s1.end(), s2.begin(), s2.end(), inserter(intersect, intersect.begin()));
    return intersect;
}

//function calculates and returns a set which is the intersection of the 4 sets
//checks if the sets are greater than 1 so the given song is not the only one in the set
set<string> smallestIntersection(set<string> valenceSet, set<string> danceSet, set<string> energySet, set<string> acousticSet) {

    set<string> intersect1; set<string> intersect2; set<string> intersect3;

    if (valenceSet.size() > 1) {
        if (danceSet.size() > 1) {
            intersect1 = intersection(valenceSet, danceSet);
            if (energySet.size() > 1) {
                intersect2 = intersection(intersect1, energySet);
                if (acousticSet.size() > 1) {
                    intersect3 = intersection(intersect2, acousticSet);
                }
            }
            else {
                if (acousticSet.size() > 1) {
                    intersect2 = intersection(intersect1, acousticSet);
                }
            }
        }
        else {
            if (energySet.size() > 1) {
                intersect1 = intersection(valenceSet, energySet);
                if (acousticSet.size() > 1) {
                    intersect2 = intersection(intersect2, acousticSet);
                }
            }
        }
    }
    else {
        if (danceSet.size() > 1) {
            if (energySet.size() > 1) {
                intersect1 = intersection(danceSet, energySet);
                if (acousticSet.size() > 1) {
                    intersect2 = intersection(intersect1, acousticSet);
                }
            }
            else {
                if (acousticSet.size() > 1) {
                    intersect1 = intersection(danceSet, acousticSet);
                }
            }
        }
        else {
            if (energySet.size() > 1) {
                if (acousticSet.size() > 1) {
                    intersect1 = intersection(energySet, acousticSet);
                }
            }
        }
    }

    if (intersect3.size() > 0) {
        return intersect3;
    }
    else if (intersect2.size() > 0) {
        return intersect2;
    }
    else if (intersect1.size() > 0) {
        return intersect1;
    }
    else if (valenceSet.size() > 1){
        return valenceSet;
    }
    else if (danceSet.size() > 1) {
        return danceSet;
    }
    else if (energySet.size() > 1) {
        return energySet;
    }
    else {
        return acousticSet;
    }
}

//Tree::Node* treeTraversal(Tree::Node* root) {

//}

int main() {

    ifstream data;
    data.open("SpotifyData3.csv");

    Tree valenceTree = Tree();
    Tree danceTree = Tree();
    Tree energyTree = Tree();
    Tree acousticnessTree = Tree();

    //given the name or ID we need to be able to find the 4 values easily
    unordered_map<string, vector<float>> IDs;   //Vector pos 0 = valence, 1 = dance, 2 = energy, 3 = acoustic, 4 = instrumentalness
    unordered_map<string, pair<string, string>> songNames;  //ID -> <name, artist>

    //"Graphs": <float upper limit, vector <string ID>>
    unordered_map<float, vector<string>> valGraph;
    unordered_map<float, vector<string>> danceGraph;
    unordered_map<float, vector<string>> energyGraph;
    unordered_map<float, vector<string>> acousticGraph;

    MakeTree(data, valenceTree, danceTree, energyTree, acousticnessTree, IDs, songNames);
    data.close();

    data.open("spotifyGenres.csv");
    unordered_map<string, vector<string>> artistGenre; //Artist, Genres
    mapArtistandGenre(data, artistGenre);
    data.close();

    //valenceTree.PrintInOrder();

    //prompt user to input names of songs they like: if possible make it a search engine where they can add and remove in GUI
    cout << "Insert ID. Type Done to conclude." << endl;
    vector<string> userLikedSongs; //used for calculating song property averages
    set<string> userLikedGenres; //used for cross-check at the end
    string ID;
    while (ID != "Done") {
        getline(cin, ID);
        if (IDs.find(ID) != IDs.end()) {
            userLikedSongs.push_back(ID);
            //Add the artists' genres into the userLikedGenres set
            string artists = songNames[ID].second;
            while (artists.find(',') != string::npos) {
                string temp = artists.substr(0, artists.find(',')); //Substrate the string in case there are multiple artists
                for (string& x : artistGenre[temp]) {                    //iterate through that artists' genres and push into the set
//                    if (x != "") //FIXME check whether or not we want to include {} genres, which are typically musicals
                    userLikedGenres.insert(x);
                }
                artists = artists.substr(artists.find(',') + 2);
            }
            artists.substr(0, artists.find(',')); //While only accounts for substrings separated by ',' - this is here to add the final artist's genres
            userLikedGenres.insert(artists);

            cout << "Successfully added " << songNames[ID].first << " by " << songNames[ID].second << endl;
        }
        else if (ID == "Done")
            break;
        else
            cout << "Sorry, we could not find that ID." << endl;
    }

    //calc average values
    float avgVal = 0.0f, avgDance = 0.0f, avgEnergy = 0.0f, avgAcoustic = 0.0f, avgInstrumentalness = 0.0f, avgSpeechiness = 0.0f;
    for (int i = 0; i < userLikedSongs.size(); i++) {
        avgVal += IDs[userLikedSongs[i]][0];
        avgDance += IDs[userLikedSongs[i]][1];
        avgEnergy += IDs[userLikedSongs[i]][2];
        avgAcoustic += IDs[userLikedSongs[i]][3];
        avgInstrumentalness += IDs[userLikedSongs[i]][4];
        avgSpeechiness += IDs[userLikedSongs[i]][5];
    }

    //Divide to get average
    avgVal /= userLikedSongs.size(); avgDance /= userLikedSongs.size(); avgEnergy /= userLikedSongs.size(); avgAcoustic /= userLikedSongs.size(); avgInstrumentalness /= userLikedSongs.size(); avgSpeechiness /= userLikedSongs.size();

    //Want to dynamically adjust this for different elements
    float range = .1f;

    //these are the sets storing the similar values to the ID entered
    set<string> valenceSet = songSuggestionSet(valenceTree, avgVal, range);
    set<string> danceSet = songSuggestionSet(danceTree, avgDance, range);
    set<string> energySet = songSuggestionSet(energyTree, avgEnergy, range);
    set<string> acousticSet = songSuggestionSet(acousticnessTree, avgAcoustic, .25f);
    cout << valenceSet.size() << " " << danceSet.size() << " " << energySet.size() << " " << acousticSet.size() << endl;

    set<string> suggestable = smallestIntersection(valenceSet, danceSet, energySet, acousticSet);
    cout << suggestable.size() << endl;

    //Check for instrumentalness and speechiness
    instrumentalAndSpeechCheck(suggestable, IDs, avgInstrumentalness, avgSpeechiness);
    cout << "instrumental " << suggestable.size() << endl;
    //Check for artist-genre cross check
    genreCrossCheck(suggestable, songNames, artistGenre, userLikedGenres);

    //FIXME, temp fix for removing same ID's in user inputted and suggestions
    for (string x : userLikedSongs) {
        suggestable.erase(x);
    }

    ofstream suggestions;
    suggestions.open("suggestions.txt");
    for (string x : suggestable) {
        x.erase(std::remove(x.begin(), x.end(), '\''), x.end());
        suggestions << songNames[x].first << " by " << songNames[x].second << endl;
//        suggestions << x << endl;
    }

    cout << "Genre: " << suggestable.size() << endl;

    return 0;
}