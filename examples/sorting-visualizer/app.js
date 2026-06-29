/**
 * SortViz — Interactive Sorting Algorithm Visualizer
 * 
 * A premium, single-page sorting visualizer built with vanilla JS.
 * Features: 4 algorithms, real-time animation, step-by-step mode,
 * comparison mode, live statistics, and glassmorphism UI.
 * 
 * @author LoopSpec Agent
 * @version 1.0.0
 */

// ============================================================
// 1. STATE MANAGEMENT
// ============================================================

/** @type {Object} Global application state */
const state = {
    array: [],
    arraySize: 30,
    speed: 'medium',
    algorithm: 'bubble',
    isSorting: false,
    isSorted: false,
    stepMode: false,
    compareMode: false,
    abortController: null,
};

/** Speed-to-delay mapping in milliseconds */
const SPEED_MAP = {
    slow: 150,
    medium: 40,
    fast: 5,
};

/** Algorithm display names and Big-O complexities */
const ALGO_INFO = {
    bubble: { name: 'Bubble Sort', complexity: 'O(n²)' },
    insertion: { name: 'Insertion Sort', complexity: 'O(n²)' },
    merge: { name: 'Merge Sort', complexity: 'O(n log n)' },
    quick: { name: 'Quick Sort', complexity: 'O(n log n)' },
};

// ============================================================
// 2. DOM REFERENCES
// ============================================================

const dom = {
    // Controls
    algorithmSelect: document.getElementById('algorithm-select'),
    sizeSlider: document.getElementById('size-slider'),
    sizeValue: document.getElementById('size-value'),
    speedSelect: document.getElementById('speed-select'),
    btnGenerate: document.getElementById('btn-generate'),
    btnSort: document.getElementById('btn-sort'),
    btnStep: document.getElementById('btn-step'),
    btnStepMode: document.getElementById('btn-step-mode'),
    btnCompare: document.getElementById('btn-compare'),
    statusBadge: document.getElementById('status-badge'),

    // Visualizers
    singleVisualizer: document.getElementById('single-visualizer'),
    singleAlgoLabel: document.getElementById('single-algo-label'),
    barContainerMain: document.getElementById('bar-container-main'),
    comparisonPanel: document.getElementById('comparison-panel'),
    barContainerA: document.getElementById('bar-container-a'),
    barContainerB: document.getElementById('bar-container-b'),
    compareAlgoA: document.getElementById('compare-algo-a'),
    compareAlgoB: document.getElementById('compare-algo-b'),

    // Stats — single mode
    statsSingle: document.getElementById('stats-single'),
    statComparisons: document.getElementById('stat-comparisons'),
    statSwaps: document.getElementById('stat-swaps'),
    statTime: document.getElementById('stat-time'),
    statComplexity: document.getElementById('stat-complexity'),

    // Stats — comparison mode
    statsComparison: document.getElementById('stats-comparison'),
    statsLabelA: document.getElementById('stats-label-a'),
    statsLabelB: document.getElementById('stats-label-b'),
    statComparisonsA: document.getElementById('stat-comparisons-a'),
    statSwapsA: document.getElementById('stat-swaps-a'),
    statTimeA: document.getElementById('stat-time-a'),
    statComplexityA: document.getElementById('stat-complexity-a'),
    statComparisonsB: document.getElementById('stat-comparisons-b'),
    statSwapsB: document.getElementById('stat-swaps-b'),
    statTimeB: document.getElementById('stat-time-b'),
    statComplexityB: document.getElementById('stat-complexity-b'),
};

// ============================================================
// 3. UTILITY FUNCTIONS
// ============================================================

/**
 * Returns a promise that resolves after the given milliseconds.
 * @param {number} ms - Delay in milliseconds
 * @returns {Promise<void>}
 */
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Gets the current delay based on the speed setting.
 * @returns {number} Delay in ms
 */
const getDelay = () => SPEED_MAP[state.speed] || SPEED_MAP.medium;

/**
 * Generates a random array of the given size with values between 5 and 100.
 * @param {number} size - Array length
 * @returns {number[]} Random array
 */
const generateArray = (size) => {
    return Array.from({ length: size }, () => Math.floor(Math.random() * 96) + 5);
};

/**
 * Creates a statistics tracking object.
 * @returns {Object} Stats object with comparisons, swaps, startTime
 */
const createStats = () => ({
    comparisons: 0,
    swaps: 0,
    startTime: performance.now(),
});

// ============================================================
// 4. STEP CONTROLLER (for step-by-step mode)
// ============================================================

/**
 * Creates a step controller that pauses execution until user clicks "Step".
 * When step mode is off, it just awaits the normal delay.
 * @returns {Object} Controller with waitForStep() method
 */
const createStepController = () => {
    let resolve = null;

    return {
        /** Promise-based wait: resolves on step click or immediately if not in step mode */
        waitForStep: async () => {
            if (!state.stepMode) {
                await delay(getDelay());
                return;
            }
            // In step mode: wait for user to click "Step"
            return new Promise((r) => {
                resolve = r;
                dom.btnStep.disabled = false;
            });
        },

        /** Called when the Step button is clicked */
        advance: () => {
            if (resolve) {
                dom.btnStep.disabled = true;
                resolve();
                resolve = null;
            }
        },
    };
};

// Global step controller instance (recreated each sort)
let stepController = createStepController();

// ============================================================
// 5. DOM RENDERING
// ============================================================

/**
 * Renders an array as bars in the given container.
 * @param {HTMLElement} container - The bar container element
 * @param {number[]} arr - The array to render
 */
const renderBars = (container, arr) => {
    container.innerHTML = '';
    const maxVal = Math.max(...arr, 1);
    arr.forEach((val, idx) => {
        const bar = document.createElement('div');
        bar.className = 'bar';
        bar.style.height = `${(val / maxVal) * 100}%`;
        bar.dataset.index = idx;
        bar.dataset.value = val;
        container.appendChild(bar);
    });
};

/**
 * Updates bar heights in an existing container (no re-creation).
 * @param {HTMLElement} container - The bar container element
 * @param {number[]} arr - The updated array
 */
const updateBars = (container, arr) => {
    const bars = container.children;
    const maxVal = Math.max(...arr, 1);
    for (let i = 0; i < arr.length; i++) {
        if (bars[i]) {
            bars[i].style.height = `${(arr[i] / maxVal) * 100}%`;
            bars[i].dataset.value = arr[i];
        }
    }
};

/**
 * Highlights specific bars with a CSS class.
 * @param {HTMLElement} container - The bar container
 * @param {number[]} indices - Indices to highlight
 * @param {string} className - CSS class to apply ('comparing', 'swapping', 'sorted', 'pivot')
 */
const highlightBars = (container, indices, className) => {
    indices.forEach((i) => {
        const bar = container.children[i];
        if (bar) bar.classList.add(className);
    });
};

/**
 * Clears a CSS class from all bars in a container.
 * @param {HTMLElement} container - The bar container
 * @param {string} className - CSS class to remove
 */
const clearHighlight = (container, className) => {
    Array.from(container.children).forEach((bar) => bar.classList.remove(className));
};

/**
 * Clears all highlight classes from all bars.
 * @param {HTMLElement} container - The bar container
 */
const clearAllHighlights = (container) => {
    Array.from(container.children).forEach((bar) => {
        bar.classList.remove('comparing', 'swapping', 'sorted', 'pivot');
    });
};

/**
 * Marks all bars as sorted (green).
 * @param {HTMLElement} container - The bar container
 */
const markAllSorted = (container) => {
    Array.from(container.children).forEach((bar, i) => {
        setTimeout(() => bar.classList.add('sorted'), i * 15);
    });
};

/**
 * Updates the stats display elements.
 * @param {Object} stats - Stats object { comparisons, swaps, startTime }
 * @param {Object} elements - DOM elements { comparisons, swaps, time, complexity }
 * @param {string} algoKey - Algorithm key for complexity lookup
 */
const updateStatsDisplay = (stats, elements, algoKey) => {
    elements.comparisons.textContent = stats.comparisons;
    elements.swaps.textContent = stats.swaps;
    const elapsed = Math.round(performance.now() - stats.startTime);
    elements.time.textContent = `${elapsed}ms`;
    elements.complexity.textContent = ALGO_INFO[algoKey]?.complexity || '—';
};

/**
 * Resets stats display to zero.
 * @param {Object} elements - DOM elements { comparisons, swaps, time, complexity }
 */
const resetStatsDisplay = (elements) => {
    elements.comparisons.textContent = '0';
    elements.swaps.textContent = '0';
    elements.time.textContent = '0ms';
    elements.complexity.textContent = '—';
};

// ============================================================
// 6. STATUS MANAGEMENT
// ============================================================

/**
 * Sets the status badge text and style.
 * @param {'ready'|'sorting'|'complete'} status
 */
const setStatus = (status) => {
    const badge = dom.statusBadge;
    badge.className = `status-badge ${status}`;
    const labels = { ready: 'Ready', sorting: 'Sorting...', complete: 'Complete' };
    badge.innerHTML = `<span class="status-dot"></span> ${labels[status]}`;
};

/**
 * Sets UI enabled/disabled state during sorting.
 * @param {boolean} sorting - Whether sorting is in progress
 */
const setUIState = (sorting) => {
    state.isSorting = sorting;
    dom.btnGenerate.disabled = sorting;
    dom.btnSort.disabled = sorting;
    dom.sizeSlider.disabled = sorting;
    dom.algorithmSelect.disabled = sorting;
    dom.speedSelect.disabled = sorting;
    dom.btnStepMode.disabled = sorting;
    dom.btnCompare.disabled = sorting;
    dom.compareAlgoA.disabled = sorting;
    dom.compareAlgoB.disabled = sorting;

    if (sorting) {
        document.body.classList.add('sorting-active');
        setStatus('sorting');
    } else {
        document.body.classList.remove('sorting-active');
    }
};

// ============================================================
// 7. SORTING ALGORITHMS (async with animation)
// ============================================================

/**
 * Bubble Sort — O(n²)
 * Repeatedly swaps adjacent elements if they are in the wrong order.
 * @param {number[]} arr - Array to sort (mutated in place)
 * @param {HTMLElement} container - Bar container for visualization
 * @param {Object} stats - Stats tracking object
 * @param {Object} step - Step controller
 * @returns {Promise<number[]>} Sorted array
 */
const bubbleSort = async (arr, container, stats, step) => {
    const n = arr.length;
    for (let i = 0; i < n - 1; i++) {
        for (let j = 0; j < n - i - 1; j++) {
            // Highlight comparing pair
            clearHighlight(container, 'comparing');
            clearHighlight(container, 'swapping');
            highlightBars(container, [j, j + 1], 'comparing');
            stats.comparisons++;

            await step.waitForStep();

            if (arr[j] > arr[j + 1]) {
                // Swap
                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
                stats.swaps++;
                highlightBars(container, [j, j + 1], 'swapping');
                updateBars(container, arr);
                await delay(Math.max(getDelay() / 2, 2));
            }

            clearHighlight(container, 'comparing');
            clearHighlight(container, 'swapping');
        }
        // Mark the last unsorted position as sorted
        highlightBars(container, [n - i - 1], 'sorted');
    }
    // Mark first element as sorted
    if (n > 0) highlightBars(container, [0], 'sorted');
    return arr;
};

/**
 * Insertion Sort — O(n²)
 * Builds the sorted array one element at a time by inserting into correct position.
 * @param {number[]} arr - Array to sort (mutated in place)
 * @param {HTMLElement} container - Bar container
 * @param {Object} stats - Stats tracking object
 * @param {Object} step - Step controller
 * @returns {Promise<number[]>} Sorted array
 */
const insertionSort = async (arr, container, stats, step) => {
    const n = arr.length;
    if (n > 0) highlightBars(container, [0], 'sorted');

    for (let i = 1; i < n; i++) {
        const key = arr[i];
        let j = i - 1;

        clearHighlight(container, 'comparing');
        clearHighlight(container, 'swapping');
        highlightBars(container, [i], 'comparing');

        await step.waitForStep();

        while (j >= 0 && arr[j] > key) {
            stats.comparisons++;
            highlightBars(container, [j], 'swapping');
            arr[j + 1] = arr[j];
            stats.swaps++;
            updateBars(container, arr);
            await delay(Math.max(getDelay() / 2, 2));
            clearHighlight(container, 'swapping');
            j--;
        }
        if (j >= 0) stats.comparisons++;

        arr[j + 1] = key;
        updateBars(container, arr);

        clearHighlight(container, 'comparing');
        // Mark sorted portion
        for (let k = 0; k <= i; k++) {
            highlightBars(container, [k], 'sorted');
        }
    }
    return arr;
};

/**
 * Merge Sort — O(n log n)
 * Divides array in half, recursively sorts, then merges.
 * Visualized by updating the original array segment after each merge.
 * @param {number[]} arr - Array to sort (mutated in place)
 * @param {HTMLElement} container - Bar container
 * @param {Object} stats - Stats tracking object
 * @param {Object} step - Step controller
 * @returns {Promise<number[]>} Sorted array
 */
const mergeSort = async (arr, container, stats, step) => {
    /**
     * Merge helper: merges arr[left..mid] and arr[mid+1..right] in place.
     * @param {number} left - Start index
     * @param {number} mid - Middle index
     * @param {number} right - End index
     */
    const merge = async (left, mid, right) => {
        const leftArr = arr.slice(left, mid + 1);
        const rightArr = arr.slice(mid + 1, right + 1);
        let i = 0, j = 0, k = left;

        while (i < leftArr.length && j < rightArr.length) {
            stats.comparisons++;

            clearHighlight(container, 'comparing');
            highlightBars(container, [left + i, mid + 1 + j], 'comparing');

            await step.waitForStep();

            if (leftArr[i] <= rightArr[j]) {
                arr[k] = leftArr[i];
                i++;
            } else {
                arr[k] = rightArr[j];
                stats.swaps++;
                j++;
            }
            updateBars(container, arr);
            k++;
        }

        while (i < leftArr.length) {
            arr[k] = leftArr[i];
            i++;
            k++;
        }

        while (j < rightArr.length) {
            arr[k] = rightArr[j];
            j++;
            k++;
        }

        updateBars(container, arr);
        clearHighlight(container, 'comparing');
    };

    /**
     * Recursive sort helper.
     * @param {number} left - Start index
     * @param {number} right - End index
     */
    const sort = async (left, right) => {
        if (left < right) {
            const mid = Math.floor((left + right) / 2);
            await sort(left, mid);
            await sort(mid + 1, right);
            await merge(left, mid, right);
        }
    };

    await sort(0, arr.length - 1);
    markAllSorted(container);
    return arr;
};

/**
 * Quick Sort — O(n log n) average
 * Selects a pivot, partitions array around it, recursively sorts partitions.
 * @param {number[]} arr - Array to sort (mutated in place)
 * @param {HTMLElement} container - Bar container
 * @param {Object} stats - Stats tracking object
 * @param {Object} step - Step controller
 * @returns {Promise<number[]>} Sorted array
 */
const quickSort = async (arr, container, stats, step) => {
    /**
     * Partition: places pivot in correct position, elements smaller to left.
     * @param {number} low - Start index
     * @param {number} high - End index (pivot)
     * @returns {Promise<number>} Pivot's final index
     */
    const partition = async (low, high) => {
        const pivot = arr[high];
        highlightBars(container, [high], 'pivot');
        let i = low - 1;

        for (let j = low; j < high; j++) {
            stats.comparisons++;

            clearHighlight(container, 'comparing');
            clearHighlight(container, 'swapping');
            highlightBars(container, [j], 'comparing');

            await step.waitForStep();

            if (arr[j] <= pivot) {
                i++;
                [arr[i], arr[j]] = [arr[j], arr[i]];
                stats.swaps++;
                highlightBars(container, [i, j], 'swapping');
                updateBars(container, arr);
                await delay(Math.max(getDelay() / 2, 2));
                clearHighlight(container, 'swapping');
            }

            clearHighlight(container, 'comparing');
        }

        [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
        stats.swaps++;
        updateBars(container, arr);
        clearHighlight(container, 'pivot');
        highlightBars(container, [i + 1], 'sorted');

        return i + 1;
    };

    /**
     * Recursive sort helper.
     * @param {number} low - Start index
     * @param {number} high - End index
     */
    const sort = async (low, high) => {
        if (low < high) {
            const pi = await partition(low, high);
            await sort(low, pi - 1);
            await sort(pi + 1, high);
        } else if (low === high && low >= 0 && low < arr.length) {
            highlightBars(container, [low], 'sorted');
        }
    };

    if (arr.length > 0) {
        await sort(0, arr.length - 1);
    }
    return arr;
};

/** Map algorithm keys to their async sort functions */
const ALGO_MAP = {
    bubble: bubbleSort,
    insertion: insertionSort,
    merge: mergeSort,
    quick: quickSort,
};

// ============================================================
// 8. SORTING ORCHESTRATION
// ============================================================

/**
 * Runs a single sorting algorithm with animation and stats.
 * @param {string} algoKey - Algorithm key ('bubble', 'insertion', etc.)
 * @param {number[]} arr - Array to sort
 * @param {HTMLElement} container - Bar container
 * @param {Object} statElements - Stats DOM elements
 * @param {Object} step - Step controller
 * @returns {Promise<void>}
 */
const runSort = async (algoKey, arr, container, statElements, step) => {
    const sortFn = ALGO_MAP[algoKey];
    if (!sortFn) return;

    const stats = createStats();
    const complexity = ALGO_INFO[algoKey]?.complexity || '—';

    // Real-time stats update interval
    const statsInterval = setInterval(() => {
        updateStatsDisplay(stats, statElements, algoKey);
    }, 50);

    try {
        await sortFn(arr, container, stats, step);
    } finally {
        clearInterval(statsInterval);
        // Final stats update
        updateStatsDisplay(stats, statElements, algoKey);
    }
};

/**
 * Handles the Sort button click — runs single or comparison mode.
 */
const handleSort = async () => {
    if (state.isSorting) return;

    setUIState(true);
    stepController = createStepController();

    try {
        if (state.compareMode) {
            // ---- COMPARISON MODE ----
            const algoA = dom.compareAlgoA.value;
            const algoB = dom.compareAlgoB.value;
            const arrA = [...state.array];
            const arrB = [...state.array];

            renderBars(dom.barContainerA, arrA);
            renderBars(dom.barContainerB, arrB);

            dom.statsLabelA.textContent = `Panel A — ${ALGO_INFO[algoA].name}`;
            dom.statsLabelB.textContent = `Panel B — ${ALGO_INFO[algoB].name}`;

            const statsA = {
                comparisons: dom.statComparisonsA,
                swaps: dom.statSwapsA,
                time: dom.statTimeA,
                complexity: dom.statComplexityA,
            };
            const statsB = {
                comparisons: dom.statComparisonsB,
                swaps: dom.statSwapsB,
                time: dom.statTimeB,
                complexity: dom.statComplexityB,
            };

            // Disable step mode in comparison mode
            const stepA = { waitForStep: async () => await delay(getDelay()), advance: () => {} };
            const stepB = { waitForStep: async () => await delay(getDelay()), advance: () => {} };

            await Promise.all([
                runSort(algoA, arrA, dom.barContainerA, statsA, stepA),
                runSort(algoB, arrB, dom.barContainerB, statsB, stepB),
            ]);
        } else {
            // ---- SINGLE MODE ----
            const algoKey = state.algorithm;
            const arr = [...state.array];

            renderBars(dom.barContainerMain, arr);

            const statElements = {
                comparisons: dom.statComparisons,
                swaps: dom.statSwaps,
                time: dom.statTime,
                complexity: dom.statComplexity,
            };

            resetStatsDisplay(statElements);
            await runSort(algoKey, arr, dom.barContainerMain, statElements, stepController);
        }

        state.isSorted = true;
        setStatus('complete');
    } catch (err) {
        console.error('Sort error:', err);
    } finally {
        setUIState(false);
        dom.btnStep.disabled = true;
    }
};

// ============================================================
// 9. EVENT HANDLERS
// ============================================================

/** Generate a new random array and render it */
const handleGenerate = () => {
    state.array = generateArray(state.arraySize);
    state.isSorted = false;
    setStatus('ready');

    if (state.compareMode) {
        renderBars(dom.barContainerA, state.array);
        renderBars(dom.barContainerB, state.array);
        resetStatsDisplay({
            comparisons: dom.statComparisonsA,
            swaps: dom.statSwapsA,
            time: dom.statTimeA,
            complexity: dom.statComplexityA,
        });
        resetStatsDisplay({
            comparisons: dom.statComparisonsB,
            swaps: dom.statSwapsB,
            time: dom.statTimeB,
            complexity: dom.statComplexityB,
        });
    } else {
        renderBars(dom.barContainerMain, state.array);
        resetStatsDisplay({
            comparisons: dom.statComparisons,
            swaps: dom.statSwaps,
            time: dom.statTime,
            complexity: dom.statComplexity,
        });
    }
};

/** Handle array size slider change */
const handleSizeChange = () => {
    state.arraySize = parseInt(dom.sizeSlider.value, 10);
    dom.sizeValue.textContent = state.arraySize;
    handleGenerate();
};

/** Handle speed select change */
const handleSpeedChange = () => {
    state.speed = dom.speedSelect.value;
};

/** Handle algorithm select change */
const handleAlgorithmChange = () => {
    state.algorithm = dom.algorithmSelect.value;
    dom.singleAlgoLabel.textContent = ALGO_INFO[state.algorithm].name;
};

/** Toggle step-by-step mode */
const handleStepModeToggle = () => {
    state.stepMode = !state.stepMode;
    dom.btnStepMode.classList.toggle('active', state.stepMode);

    if (!state.stepMode) {
        dom.btnStep.disabled = true;
    }
};

/** Toggle comparison mode */
const handleCompareToggle = () => {
    state.compareMode = !state.compareMode;
    dom.btnCompare.classList.toggle('active', state.compareMode);

    // Toggle visibility
    dom.singleVisualizer.style.display = state.compareMode ? 'none' : 'flex';
    dom.comparisonPanel.classList.toggle('active', state.compareMode);
    dom.statsSingle.style.display = state.compareMode ? 'none' : '';
    dom.statsComparison.classList.toggle('active', state.compareMode);

    // Disable step mode in compare mode
    if (state.compareMode && state.stepMode) {
        handleStepModeToggle();
    }
    dom.btnStepMode.disabled = state.compareMode;

    handleGenerate();
};

// ============================================================
// 10. INITIALIZATION
// ============================================================

/**
 * Initialize the app: bind events, generate first array.
 */
const init = () => {
    // Bind control events
    dom.btnGenerate.addEventListener('click', handleGenerate);
    dom.btnSort.addEventListener('click', handleSort);
    dom.btnStep.addEventListener('click', () => stepController.advance());
    dom.btnStepMode.addEventListener('click', handleStepModeToggle);
    dom.btnCompare.addEventListener('click', handleCompareToggle);
    dom.sizeSlider.addEventListener('input', handleSizeChange);
    dom.speedSelect.addEventListener('change', handleSpeedChange);
    dom.algorithmSelect.addEventListener('change', handleAlgorithmChange);

    // Set initial state from DOM defaults
    state.algorithm = dom.algorithmSelect.value;
    state.speed = dom.speedSelect.value;
    state.arraySize = parseInt(dom.sizeSlider.value, 10);
    dom.singleAlgoLabel.textContent = ALGO_INFO[state.algorithm].name;

    // Generate initial array
    handleGenerate();

    // Set initial complexity
    dom.statComplexity.textContent = ALGO_INFO[state.algorithm].complexity;
};

// Start when DOM is ready
document.addEventListener('DOMContentLoaded', init);
