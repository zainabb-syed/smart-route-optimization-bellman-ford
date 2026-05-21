#include <stdio.h>

#define V 7
#define E 10
#define INF 99999

// =========================================================
// Structure for Graph Edge
// =========================================================

struct Edge {

    int source;
    int destination;
    int weight;
};


// =========================================================
// Function to Print Shortest Path
// =========================================================

void printPath(int parent[], int vertex) {

    if(parent[vertex] == -1) {

        printf("%d ", vertex);
        return;
    }

    printPath(parent, parent[vertex]);

    printf("-> %d ", vertex);
}


// =========================================================
// Bellman Ford Algorithm
// =========================================================

void bellmanFord(struct Edge edges[], int source) {

    int distance[V];
    int parent[V];

    // =====================================================
    // Initialize Distances and Parents
    // =====================================================

    for(int i = 0; i < V; i++) {

        distance[i] = INF;

        parent[i] = -1;
    }

    distance[source] = 0;


    // =====================================================
    // Relax All Edges V-1 Times
    // =====================================================

    for(int i = 1; i <= V - 1; i++) {

        for(int j = 0; j < E; j++) {

            int u = edges[j].source;
            int v = edges[j].destination;
            int w = edges[j].weight;

            if(distance[u] != INF &&
               distance[u] + w < distance[v]) {

                distance[v] = distance[u] + w;

                parent[v] = u;
            }
        }
    }


    // =====================================================
    // Negative Cycle Detection
    // =====================================================

    for(int j = 0; j < E; j++) {

        int u = edges[j].source;
        int v = edges[j].destination;
        int w = edges[j].weight;

        if(distance[u] != INF &&
           distance[u] + w < distance[v]) {

            printf("\nNegative Weight Cycle Detected\n");

            return;
        }
    }


    // =====================================================
    // City Names
    // =====================================================

    char *cities[V] = {

        "Bangalore",
        "Hyderabad",
        "Chennai",
        "Mumbai",
        "Delhi",
        "Pune",
        "Kolkata"
    };


    // =====================================================
    // Display Results
    // =====================================================

    printf("\n========================================");
    printf("\nShortest Route Details");
    printf("\n========================================\n");

    for(int i = 0; i < V; i++) {

        printf("\nDestination : %s\n", cities[i]);

        printf("Distance    : ");

        if(distance[i] == INF)
            printf("No Route Available\n");

        else
            printf("%d km\n", distance[i]);

        printf("Path        : ");

        if(distance[i] == INF)
            printf("No Path\n");

        else
            printPath(parent, i);

        printf("\n");
    }
}


// =========================================================
// Main Function
// =========================================================

int main() {

    // =====================================================
    // Graph Edges
    // =====================================================

    struct Edge edges[E] = {

        {0, 1, 4},
        {0, 2, 2},
        {2, 1, 1},
        {1, 3, 2},
        {2, 3, 7},
        {1, 4, 6},
        {3, 5, 3},
        {5, 4, 2},
        {4, 6, 5},
       // {6,3,4}
        {6, 3, -20},
       // {3,1, -3} // Negative weight edge for testing
    };


    int source;


    // =====================================================
    // Vertex Mapping
    // =====================================================

    printf("\n========================================");
    printf("\nCity Mapping");
    printf("\n========================================\n");

    printf("0 -> Bangalore\n");
    printf("1 -> Hyderabad\n");
    printf("2 -> Chennai\n");
    printf("3 -> Mumbai\n");
    printf("4 -> Delhi\n");
    printf("5 -> Pune\n");
    printf("6 -> Kolkata\n");


    // =====================================================
    // User Input
    // =====================================================

    printf("\nEnter Source Vertex (0 - 6) : ");

    scanf("%d", &source);


    // =====================================================
    // Run Bellman Ford Algorithm
    // =====================================================

    bellmanFord(edges, source);

    return 0;
}