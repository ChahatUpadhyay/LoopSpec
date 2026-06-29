/**
 * Node.js Sorting Algorithm Test Suite
 * Runs the same tests as test.html but in Node.js for CLI verification.
 * Usage: node test-node.js
 */

// ============================================================
// PURE SORTING ALGORITHMS (identical to test.html)
// ============================================================

const SortAlgorithms = {
    bubbleSort(arr) {
        const a = [...arr];
        const n = a.length;
        let comparisons = 0, swaps = 0;
        for (let i = 0; i < n - 1; i++) {
            for (let j = 0; j < n - i - 1; j++) {
                comparisons++;
                if (a[j] > a[j + 1]) {
                    [a[j], a[j + 1]] = [a[j + 1], a[j]];
                    swaps++;
                }
            }
        }
        return { sorted: a, comparisons, swaps };
    },

    insertionSort(arr) {
        const a = [...arr];
        const n = a.length;
        let comparisons = 0, swaps = 0;
        for (let i = 1; i < n; i++) {
            const key = a[i];
            let j = i - 1;
            while (j >= 0 && a[j] > key) {
                comparisons++;
                a[j + 1] = a[j];
                swaps++;
                j--;
            }
            if (j >= 0) comparisons++;
            a[j + 1] = key;
        }
        return { sorted: a, comparisons, swaps };
    },

    mergeSort(arr) {
        const a = [...arr];
        let comparisons = 0, swaps = 0;

        const merge = (left, right) => {
            const result = [];
            let i = 0, j = 0;
            while (i < left.length && j < right.length) {
                comparisons++;
                if (left[i] <= right[j]) {
                    result.push(left[i++]);
                } else {
                    result.push(right[j++]);
                    swaps++;
                }
            }
            return result.concat(left.slice(i)).concat(right.slice(j));
        };

        const sort = (arr) => {
            if (arr.length <= 1) return arr;
            const mid = Math.floor(arr.length / 2);
            const left = sort(arr.slice(0, mid));
            const right = sort(arr.slice(mid));
            return merge(left, right);
        };

        const sorted = sort(a);
        return { sorted, comparisons, swaps };
    },

    quickSort(arr) {
        const a = [...arr];
        let comparisons = 0, swaps = 0;

        const partition = (low, high) => {
            const pivot = a[high];
            let i = low - 1;
            for (let j = low; j < high; j++) {
                comparisons++;
                if (a[j] <= pivot) {
                    i++;
                    [a[i], a[j]] = [a[j], a[i]];
                    swaps++;
                }
            }
            [a[i + 1], a[high]] = [a[high], a[i + 1]];
            swaps++;
            return i + 1;
        };

        const sort = (low, high) => {
            if (low < high) {
                const pi = partition(low, high);
                sort(low, pi - 1);
                sort(pi + 1, high);
            }
        };

        if (a.length > 0) sort(0, a.length - 1);
        return { sorted: a, comparisons, swaps };
    }
};

// ============================================================
// TEST FRAMEWORK
// ============================================================

let totalPassed = 0;
let totalFailed = 0;

const arraysEqual = (a, b) => {
    if (a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) {
        if (a[i] !== b[i]) return false;
    }
    return true;
};

const logResult = (name, passed, detail = '') => {
    const icon = passed ? '✅' : '❌';
    if (passed) totalPassed++; else totalFailed++;
    console.log(`  ${icon} ${name}${detail ? ' — ' + detail : ''}`);
};

// ============================================================
// TEST DATA
// ============================================================

const testCases = [
    { name: 'Random array', input: [38, 27, 43, 3, 9, 82, 10] },
    { name: 'Already sorted', input: [1, 2, 3, 4, 5, 6, 7, 8] },
    { name: 'Reverse sorted', input: [8, 7, 6, 5, 4, 3, 2, 1] },
    { name: 'Single element', input: [42] },
    { name: 'Empty array', input: [] },
    { name: 'Duplicates', input: [5, 3, 5, 1, 3, 2, 5, 1] },
    { name: 'All same', input: [7, 7, 7, 7, 7] },
    { name: 'Two elements', input: [2, 1] },
    { name: 'Large random (50)', input: Array.from({ length: 50 }, () => Math.floor(Math.random() * 100) + 1) },
    { name: 'Large random (100)', input: Array.from({ length: 100 }, () => Math.floor(Math.random() * 200) + 1) },
];

// ============================================================
// RUN TESTS
// ============================================================

const algorithms = ['bubbleSort', 'insertionSort', 'mergeSort', 'quickSort'];

console.log('\n🧪 Sorting Algorithm Test Suite (Node.js)\n');
console.log('='.repeat(60));

for (const algo of algorithms) {
    console.log(`\n📊 ${algo}`);
    for (const tc of testCases) {
        const expected = [...tc.input].sort((a, b) => a - b);
        try {
            const result = SortAlgorithms[algo](tc.input);
            const passed = arraysEqual(result.sorted, expected);
            logResult(
                `${tc.name}`,
                passed,
                passed
                    ? `${result.comparisons} cmp, ${result.swaps} swaps`
                    : `Expected [${expected}], got [${result.sorted}]`
            );
        } catch (err) {
            logResult(`${tc.name}`, false, `Error: ${err.message}`);
        }
    }
}

// Cross-algorithm consistency
console.log('\n🔗 Cross-Algorithm Consistency');
for (const tc of testCases) {
    const results = algorithms.map(algo => SortAlgorithms[algo](tc.input).sorted);
    const allMatch = results.every(r => arraysEqual(r, results[0]));
    logResult(
        `All agree — ${tc.name}`,
        allMatch,
        allMatch ? 'Identical output' : 'MISMATCH'
    );
}

// Stats sanity
console.log('\n📈 Statistics Sanity Checks');
const reverseResult = SortAlgorithms.bubbleSort([5, 4, 3, 2, 1]);
logResult('Bubble reverse — cmp = n*(n-1)/2', reverseResult.comparisons === 10, `Got ${reverseResult.comparisons}`);

const sortedResult = SortAlgorithms.bubbleSort([1, 2, 3, 4, 5]);
logResult('Bubble sorted — zero swaps', sortedResult.swaps === 0, `Got ${sortedResult.swaps}`);

// Summary
console.log('\n' + '='.repeat(60));
const total = totalPassed + totalFailed;
if (totalFailed === 0) {
    console.log(`\n✅ ALL ${total} TESTS PASSED\n`);
    process.exit(0);
} else {
    console.log(`\n❌ ${totalFailed} of ${total} tests FAILED\n`);
    process.exit(1);
}
