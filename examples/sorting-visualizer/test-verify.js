// Sorting Algorithm Verification Script (JScript for cscript.exe)
// Usage: cscript //nologo //E:JScript test-verify.js

var algorithms = {
    bubbleSort: function(arr) {
        var a = arr.slice(); var n = a.length; var cmp = 0; var swp = 0;
        for (var i = 0; i < n-1; i++) {
            for (var j = 0; j < n-i-1; j++) {
                cmp++;
                if (a[j] > a[j+1]) { var t=a[j]; a[j]=a[j+1]; a[j+1]=t; swp++; }
            }
        }
        return {sorted:a, comparisons:cmp, swaps:swp};
    },
    insertionSort: function(arr) {
        var a = arr.slice(); var n = a.length; var cmp = 0; var swp = 0;
        for (var i = 1; i < n; i++) {
            var key = a[i]; var j = i-1;
            while (j >= 0 && a[j] > key) { cmp++; a[j+1] = a[j]; swp++; j--; }
            if (j >= 0) cmp++;
            a[j+1] = key;
        }
        return {sorted:a, comparisons:cmp, swaps:swp};
    },
    mergeSort: function(arr) {
        var cmp = 0; var swp = 0;
        function merge(left, right) {
            var result = []; var i = 0; var j = 0;
            while (i < left.length && j < right.length) {
                cmp++;
                if (left[i] <= right[j]) { result.push(left[i++]); }
                else { result.push(right[j++]); swp++; }
            }
            while(i<left.length) result.push(left[i++]);
            while(j<right.length) result.push(right[j++]);
            return result;
        }
        function sort(a) {
            if (a.length <= 1) return a;
            var mid = Math.floor(a.length/2);
            return merge(sort(a.slice(0,mid)), sort(a.slice(mid)));
        }
        var sorted = sort(arr.slice());
        return {sorted:sorted, comparisons:cmp, swaps:swp};
    },
    quickSort: function(arr) {
        var a = arr.slice(); var cmp = 0; var swp = 0;
        function partition(lo,hi) {
            var pivot=a[hi]; var i=lo-1;
            for(var j=lo;j<hi;j++){
                cmp++;
                if(a[j]<=pivot){i++;var t=a[i];a[i]=a[j];a[j]=t;swp++;}
            }
            var t2=a[i+1];a[i+1]=a[hi];a[hi]=t2;swp++;
            return i+1;
        }
        function sort(lo,hi) {
            if(lo<hi){var pi=partition(lo,hi);sort(lo,pi-1);sort(pi+1,hi);}
        }
        if(a.length>0) sort(0,a.length-1);
        return {sorted:a, comparisons:cmp, swaps:swp};
    }
};

var testCases = [
    {name:"Random", input:[38,27,43,3,9,82,10]},
    {name:"Sorted", input:[1,2,3,4,5,6,7,8]},
    {name:"Reverse", input:[8,7,6,5,4,3,2,1]},
    {name:"Single", input:[42]},
    {name:"Empty", input:[]},
    {name:"Dupes", input:[5,3,5,1,3,2,5,1]},
    {name:"AllSame", input:[7,7,7,7,7]},
    {name:"Two", input:[2,1]},
    {name:"Large", input:[64,25,12,22,11,90,45,33,78,56,67,23,89,34,15,44,71,82,9,61]}
];

var passed = 0;
var failed = 0;
var algoNames = ["bubbleSort","insertionSort","mergeSort","quickSort"];

for (var ai=0; ai<algoNames.length; ai++) {
    var algo = algoNames[ai];
    WScript.Echo("\n=== " + algo + " ===");
    for (var ti=0; ti<testCases.length; ti++) {
        var tc = testCases[ti];
        var expected = tc.input.slice().sort(function(a,b){return a-b;});
        var result = algorithms[algo](tc.input);
        var ok = true;
        if (result.sorted.length !== expected.length) ok = false;
        else {
            for(var k=0;k<expected.length;k++){
                if(result.sorted[k]!==expected[k]){ok=false;break;}
            }
        }
        if(ok) { passed++; WScript.Echo("  PASS: " + tc.name + " (" + result.comparisons + " cmp, " + result.swaps + " swaps)"); }
        else { failed++; WScript.Echo("  FAIL: " + tc.name + " expected=[" + expected + "] got=[" + result.sorted + "]"); }
    }
}

WScript.Echo("\n" + "=".repeat ? "============" : "============");
if(failed===0) { WScript.Echo("ALL " + passed + " TESTS PASSED"); }
else { WScript.Echo(failed + " of " + (passed+failed) + " FAILED"); }
WScript.Quit(failed > 0 ? 1 : 0);
