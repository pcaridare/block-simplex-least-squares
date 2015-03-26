/*
 * isotonic_regression.h
 *
 *  Created on: Mar 10, 2015
 *      Author: jeromethai
 */

 #include <iostream> // std::cout

 using std::cout;
using std::endl;

void isotonic_regression(double *y, int start, int end, int *weight, int update) {
    // Do isotonic regression from start to end (end not included)
    // if update == 1, return an updated vector y vector
    double numerator, previous;
    int i, j, k, pooled, denominator;
    while (1) {
        // repeat until there are no more adjacent violators.
        i = start;
        pooled = 0;
        while (i < end) {
            k = i + weight[i];
            previous = y[i];
            while (k < end && y[k] <= previous) {
                previous = y[k];
                k += weight[k];
            }
            if (y[i] != previous) {
                // y[i:k + 1] is a decreasing subsequence, so
                // replace each point in the subsequence with the
                // weighted average of the subsequence.
                numerator = 0.0;
                denominator = 0;
                j = i;
                while (j < k) {
                    numerator += y[j] * weight[j];
                    denominator += weight[j];
                    j += weight[j];
                }
                y[i] = numerator / denominator;
                weight[i] = denominator;
                pooled = 1;
            }
            i = k;
        }
        // Check for convergence
        if (pooled == 0) break;
    }
    if (update) {
        i = start;
        while (i < end) {
            k = i + weight[i];
            for (j = i + 1; j < k; j++) y[j] = y[i];
            i += weight[i];
        }
    }    
}


void isotonic_regression_2(double *y, int start, int end) {
    double numerator, average;
    int i, j, k, pooled;
    end -= 1;
    while (1) {
        i = start;
        pooled = 0;
        while (i < end) {
            k = i;
            while (k < end && y[k] >= y[k+1]) k += 1;
            if (y[i] != y[k]) {
                numerator = 0.0;
                for (j=i; j<k+1; j++) numerator += y[j];
                average = numerator/(k+1-i);
                for (j=i; j<k+1; j++) y[j] = average;
                pooled = 1;
            }
            i = k + 1;
        }
        if (pooled == 0) break;
    }
}


void isotonic_regression_multi(double *y, int *blocks, int numblocks, int n, int *weight, int update) {
	// Do multiple iso tonic regressions where blocks is an array of integers 
	// that contains the first index of each block and n the length of the array
	for (int i = 0; i < numblocks-1; i++) {
		isotonic_regression(y, blocks[i], blocks[i+1], weight, update);
	}
	isotonic_regression(y, blocks[numblocks-1], n, weight, update);
}


void isotonic_regression_multi_2(double *y, int *blocks, int numblocks, int n) {
    // Do multiple iso tonic regressions where blocks is an array of integers 
    // that contains the first index of each block and n the length of the array
    for (int i = 0; i < numblocks-1; i++) {
        isotonic_regression_2(y, blocks[i], blocks[i+1]);
    }
    isotonic_regression_2(y, blocks[numblocks-1], n);
}


int test_isotonic_regression() {
    cout << "Test isotonic_regression." << endl;
	double doubleArray[] = {4., 5., 1., 6., 8., 7.};
    int weight[] = {1, 1, 1, 1, 1, 1};
    int weight2[] = {1, 1, 1, 1, 1, 1};
    int weight3[] = {1, 1, 1, 1, 1, 1};
    int blocks[] = {0};
    int blocks2[] = {0, 2, 4};
    int update = 1;

    isotonic_regression(doubleArray, 0, 6, weight, update);
    cout << "Projected block-vector is this." << endl;
    for (size_t i = 0; i != 6; ++i)
        cout << doubleArray[i] << " "; // should get 3.3, 3.3, 3.3, 6. 7.5, 7.5
        cout << endl;

    double doubleArray2[] = {4., 5., 1., 6., 8., 7.};
    isotonic_regression_multi(doubleArray2, blocks, 1, 6, weight2, update);
    cout << "Projected block-vector is this." << endl;
    for (size_t i = 0; i != 6; ++i)
        cout << doubleArray2[i] << " "; // should get 3.3, 3.3, 3.3, 6. 7.5, 7.5
        cout << endl;

    double doubleArray3[] = {4., 5., 1., 6., 8., 7.};
    isotonic_regression_multi(doubleArray3, blocks2, 3, 6, weight3, update);
    cout << "Projected block-vector is this." << endl;
    for (size_t i = 0; i != 6; ++i)
        cout << doubleArray3[i] << " "; // should get 4, 5, 1, 6, 7.5, 7.5
        cout << endl;

    return 0;
}

int test_isotonic_regression_2() {
    cout << "Test isotonic_regression_2." << endl;
    double doubleArray[] = {4., 5., 1., 6., 8., 7.};
    int blocks[] = {0};
    int blocks2[] = {0, 2, 4};

    isotonic_regression_2(doubleArray, 0, 6);
    cout << "Projected block-vector is this." << endl;
    for (size_t i = 0; i != 6; ++i)
        cout << doubleArray[i] << " "; // should get 3.3, 3.3, 3.3, 6. 7.5, 7.5
        cout << endl;

    double doubleArray2[] = {4., 5., 1., 6., 8., 7.};
    isotonic_regression_multi_2(doubleArray2, blocks, 1, 6);
    cout << "Projected block-vector is this." << endl;
    for (size_t i = 0; i != 6; ++i)
        cout << doubleArray2[i] << " "; // should get 3.3, 3.3, 3.3, 6. 7.5, 7.5
        cout << endl;

    double doubleArray3[] = {4., 5., 1., 6., 8., 7.};
    isotonic_regression_multi_2(doubleArray3, blocks2, 3, 6);
    cout << "Projected block-vector is this." << endl;
    for (size_t i = 0; i != 6; ++i)
        cout << doubleArray3[i] << " "; // should get 4, 5, 1, 6, 7.5, 7.5
        cout << endl;

    return 0;
}