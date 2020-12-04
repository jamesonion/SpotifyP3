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
void MakeTree(ifstream &file, Tree &valenceTree, Tree &danceTree, Tree &energyTree, Tree &acousticnessTree, unordered_map<string, vector<double>> &IDs, unordered_map<string, pair<string, string>>& songNames) {
    if (file.is_open()) {
        string endLine;
        getline(file, endLine); // get rid of header line
        double valence; // 1st column
        double energy; // 7th column
        double danceability; // 5th column
        double acousticness; // 10th column
        string temp;
        string ID; // 9th column
        string name; // 15th column
        string artist; //last column
        while (!file.eof()) {
            getline(file, temp, ',');
            try {
                valence = stod(temp);
            }
            catch (const invalid_argument &e) {
                break;
            }

            getline(file, temp, ',');
            danceability = stod(temp);

            getline(file, temp, ',');
            energy = stod(temp);

            getline(file, ID, ',');
            getline(file, temp, ',');
            acousticness = stod(temp);

            getline(file, name, ','); // if the name has a comma in it there is a bug
            getline(file, artist); // if the name has a comma in it there is a bug

            valenceTree.insert(ID, valence);
            danceTree.insert(ID, danceability);
            energyTree.insert(ID, energy);
            acousticnessTree.insert(ID, acousticness);
            IDs[ID].push_back(valence);
            IDs[ID].push_back(danceability);
            IDs[ID].push_back(energy);
            IDs[ID].push_back(acousticness);
            songNames[ID] = make_pair(name, artist);
        }

    }
}

//recursive function to fill set
void songSuggestionSetRec(Tree::Node* curr, set<string>& suggested, double upper, double lower) {
    if (curr == nullptr) {

    }
    else {
        //if value is inside of range and the node isn't null insert the ID into the set then call function again
        if (curr->left != nullptr && curr->left->value <= upper && curr->left->value >= lower) {
            suggested.insert(curr->left->ID);
            songSuggestionSetRec(curr->left, suggested, upper, lower);
        }
        if (curr->right != nullptr && curr->right->value <= upper && curr->right->value >= lower) {
            suggested.insert(curr->right->ID);
            songSuggestionSetRec(curr->right, suggested, upper, lower);
        }
    }
}
//creates set for the given value paramter
//sets will contain the ID's of songs
//this function is somewhat inconcsistent might need to be changed in some ways like finding where to start
set<string> songSuggestionSet(Tree& tree, double value, double range) {
    //traverse the tree
    //new set is created to contain the similar values
    set<string> suggested;
    //the range for the values to be added to the set is from lowerLimit to upperLimit
    double lowerLimit = value - range;
    if (lowerLimit < 0)
        lowerLimit = 0;
    double upperLimit = value + range;
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
    suggested.insert(temp->ID);
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
set<string> smallestIntersection(set<string>& valenceSet, set<string>& danceSet, set<string>& energySet, set<string>& acousticSet) {

    set<string> intersect1;
    set<string> intersect2;
    set<string> intersect3;

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
                    intersect3 = intersection(intersect2, acousticSet);
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
    else {
        return valenceSet;
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
    unordered_map<string, vector<double>> IDs;

    //ID -> <name, artist>
    unordered_map<string, pair<string, string>> songNames;
    //Vector pos 0 = valence, 1 = dance, 2 = energy, 3 = instrumental

    //"Graphs": <double upper limit, vector <pair <string ID, double value>>>
    ///FIXME is the second double necessary? If we can find the values based solely off ID then just store that
    unordered_map<double, vector<pair<string, double>>> valGraph;
    unordered_map<double, vector<pair<string, double>>> danceGraph;
    unordered_map<double, vector<pair<string, double>>> energyGraph;
    unordered_map<double, vector<pair<string, double>>> instrumentalGraph;
    MakeTree(data, valenceTree, danceTree, energyTree, acousticnessTree, IDs, songNames);
    data.close();


    //valenceTree.PrintInOrder();
    //prompt user to input names of songs they like: if possible make it a search engine where they can add and remove in GUI

    cout << "Insert ID. Type Done to conclude." << endl;
    vector<string> userLikedSongs;
    string ID;
    while (ID != "Done") {
        getline(cin, ID);
        if (IDs.find(ID) != IDs.end()) {
            userLikedSongs.push_back(ID);
            ///FIXME remove []'s and 's from artist names
            cout << "Successfully added " << songNames[ID].first << " by " << songNames[ID].second << endl;
        }
        else if (ID == "Done")
            break;
        else
            cout << "Sorry we could not find that ID" << endl;
    }

    //see if we can manage this
    double range = 0.05;

    //calc average values
    double avgVal = 0, avgDance = 0, avgEnergy = 0, avgAcoustic = 0;
    for (int i = 0; i < userLikedSongs.size(); i++) {
        avgVal += IDs[userLikedSongs[i]][0];
        avgDance += IDs[userLikedSongs[i]][1];
        avgEnergy += IDs[userLikedSongs[i]][2];
        avgAcoustic += IDs[userLikedSongs[i]][3];
    }

    avgVal /= userLikedSongs.size();
    avgDance /= userLikedSongs.size();
    avgEnergy /= userLikedSongs.size();
    avgAcoustic /= userLikedSongs.size();

    //these are the sets storing the similar values to the ID entered
    set<string> valenceSet = songSuggestionSet(valenceTree, avgVal, range);
    set<string> danceSet = songSuggestionSet(danceTree, avgDance, range);
    set<string> energySet = songSuggestionSet(energyTree, avgEnergy, range);
    set<string> acousticSet = songSuggestionSet(acousticnessTree, avgAcoustic, range);
    cout << valenceSet.size() << " " << danceSet.size() << " " << energySet.size() << " " << acousticSet.size() << endl;

    set<string> suggestable = smallestIntersection(valenceSet, danceSet, energySet, acousticSet);

    //cout << intersect1.size() << " " << intersect2.size() << " " << intersect3.size() << endl;
    cout << suggestable.size() << endl;

    return 0;
}