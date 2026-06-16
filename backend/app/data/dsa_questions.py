# ═══════════════════════════════════════════════════════════════
# BUILT-IN QUESTION BANK (50 problems, organized by topic)
# These are used when you want EXACT problems, not LLM-generated
# ═══════════════════════════════════════════════════════════════
 
QUESTION_BANK = {
    "arrays": {
        "easy": [
            {
                "id": "arr_e1",
                "title": "Two Sum",
                "problem": """Given an array of integers nums and an integer target,
return indices of the two numbers that add up to target.
You may assume each input has exactly one solution.
You may not use the same element twice.
 
Example 1:
  Input:  nums = [2, 7, 11, 15], target = 9
  Output: [0, 1]
  Explanation: nums[0] + nums[1] = 2 + 7 = 9
 
Example 2:
  Input:  nums = [3, 2, 4], target = 6
  Output: [1, 2]
 
Constraints:
  - 2 <= nums.length <= 10^4
  - -10^9 <= nums[i] <= 10^9
  - Only one valid answer exists""",
                "approach": "HashMap: store {value: index} as you iterate",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "companies": ["Amazon", "Google", "Microsoft"],
                "hints": [
                    "Think about what complement you need for each number",
                    "Use a dictionary to store numbers you've already seen",
                    "For each number x, check if (target - x) exists in your dictionary"
                ],
                "solution": """def two_sum(nums, target):
    seen = {}  # value: index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []"""
            },
            {
                "id": "arr_e2",
                "title": "Maximum Subarray (Kadane's Algorithm)",
                "problem": """Given an integer array nums, find the subarray with the
largest sum and return its sum.
 
Example 1:
  Input:  nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
  Output: 6
  Explanation: Subarray [4, -1, 2, 1] has the largest sum = 6
 
Example 2:
  Input:  nums = [1]
  Output: 1
 
Example 3:
  Input:  nums = [5, 4, -1, 7, 8]
  Output: 23
 
Constraints:
  - 1 <= nums.length <= 10^5
  - -10^4 <= nums[i] <= 10^4""",
                "approach": "Kadane's: track current_sum and max_sum",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "companies": ["Amazon", "Infosys", "TCS"],
                "hints": [
                    "For each element, decide: extend the current subarray OR start fresh?",
                    "current_sum = max(num, current_sum + num)",
                    "Keep track of the global maximum throughout"
                ],
                "solution": """def max_subarray(nums):
    current_sum = nums[0]
    max_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum"""
            }
        ],
        "medium": [
            {
                "id": "arr_m1",
                "title": "3Sum",
                "problem": """Given an integer array nums, return all triplets [nums[i], nums[j], nums[k]]
such that i != j != k and nums[i] + nums[j] + nums[k] == 0.
The solution set must not contain duplicate triplets.
 
Example 1:
  Input:  nums = [-1, 0, 1, 2, -1, -4]
  Output: [[-1, -1, 2], [-1, 0, 1]]
 
Example 2:
  Input:  nums = [0, 0, 0]
  Output: [[0, 0, 0]]
 
Constraints:
  - 3 <= nums.length <= 3000
  - -10^5 <= nums[i] <= 10^5""",
                "approach": "Sort + Two Pointers: fix one element, use two-pointer for the rest",
                "time_complexity": "O(n²)",
                "space_complexity": "O(1) ignoring output",
                "companies": ["Google", "Amazon", "Adobe"],
                "hints": [
                    "Sort the array first — this helps with duplicates and two-pointer technique",
                    "Fix index i, then use two pointers (left=i+1, right=n-1) to find pairs",
                    "Skip duplicate values of i, left, and right to avoid duplicate triplets"
                ],
                "solution": """def three_sum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]:  # skip duplicates
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left+1]: left += 1
                while left < right and nums[right] == nums[right-1]: right -= 1
                left += 1; right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return result"""
            }
        ],
        "hard": [
            {
                "id": "arr_h1",
                "title": "Trapping Rain Water",
                "problem": """Given n non-negative integers representing an elevation map
where the width of each bar is 1, compute how much water it can trap after raining.
 
Example 1:
  Input:  height = [0,1,0,2,1,0,1,3,2,1,2,1]
  Output: 6
 
Example 2:
  Input:  height = [4,2,0,3,2,5]
  Output: 9
 
Constraints:
  - n == height.length
  - 1 <= n <= 2 * 10^4
  - 0 <= height[i] <= 10^5""",
                "approach": "Two Pointers: track left_max and right_max, move the smaller side",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "companies": ["Google", "Amazon", "Microsoft"],
                "hints": [
                    "Water at position i = min(max_left, max_right) - height[i]",
                    "Use two pointers from both ends, move the side with smaller max",
                    "The pointer with smaller max is the bottleneck — process it first"
                ],
                "solution": """def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    return water"""
            }
        ]
    },
    "strings": {
        "easy": [
            {
                "id": "str_e1",
                "title": "Valid Palindrome",
                "problem": """A phrase is a palindrome if, after converting all uppercase letters to lowercase
and removing all non-alphanumeric characters, it reads the same forward and backward.
 
Given a string s, return true if it is a palindrome, or false otherwise.
 
Example 1:
  Input:  s = "A man, a plan, a canal: Panama"
  Output: true
 
Example 2:
  Input:  s = "race a car"
  Output: false
 
Constraints:
  - 1 <= s.length <= 2 * 10^5
  - s consists only of printable ASCII characters""",
                "approach": "Two Pointers: clean string → check from both ends",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "companies": ["TCS", "Infosys", "Wipro"],
                "hints": [
                    "Filter out non-alphanumeric characters and convert to lowercase",
                    "Use two pointers: one from start, one from end",
                    "Stop when they meet in the middle"
                ],
                "solution": """def is_palindrome(s):
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]
 
# Two-pointer approach (O(1) space):
def is_palindrome_optimal(s):
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum(): left += 1
        while left < right and not s[right].isalnum(): right -= 1
        if s[left].lower() != s[right].lower(): return False
        left += 1; right -= 1
    return True"""
            }
        ]
    },
    "linked_list": {
        "easy": [
            {
                "id": "ll_e1",
                "title": "Reverse Linked List",
                "problem": """Given the head of a singly linked list, reverse the list,
and return the reversed list.
 
Example 1:
  Input:  head = [1, 2, 3, 4, 5]
  Output: [5, 4, 3, 2, 1]
 
Example 2:
  Input:  head = [1, 2]
  Output: [2, 1]
 
Constraints:
  - Number of nodes: 0 to 5000
  - -5000 <= Node.val <= 5000""",
                "approach": "Iterative: use prev, curr, next pointers",
                "time_complexity": "O(n)",
                "space_complexity": "O(1) iterative, O(n) recursive",
                "companies": ["Microsoft", "TCS", "Infosys"],
                "hints": [
                    "Use three pointers: prev=None, curr=head, next=None",
                    "For each node: save next, point curr.next to prev, advance both",
                    "Return prev when curr becomes None"
                ],
                "solution": """# Iterative — O(1) space
def reverse_list(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev
 
# Recursive — O(n) space
def reverse_list_recursive(head):
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head"""
            }
        ],
        "medium": [
            {
                "id": "ll_m1",
                "title": "Detect Cycle in Linked List",
                "problem": """Given head, the head of a linked list, determine if the linked list has a cycle.
There is a cycle if some node can be reached again by continuously following the next pointer.
 
Return true if there is a cycle, false otherwise.
 
Example 1:
  Input:  head = [3,2,0,-4], pos = 1 (tail connects to index 1)
  Output: true
 
Example 2:
  Input:  head = [1,2], pos = 0
  Output: true
 
Example 3:
  Input:  head = [1], pos = -1
  Output: false
 
Constraints:
  - Number of nodes: 0 to 10^4""",
                "approach": "Floyd's Cycle Detection: slow pointer moves 1, fast moves 2",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "companies": ["Amazon", "Microsoft", "Flipkart"],
                "hints": [
                    "Think of two runners on a track — the faster one will catch the slower one if there's a loop",
                    "Move slow pointer by 1 step, fast pointer by 2 steps each iteration",
                    "If fast and slow meet → cycle. If fast reaches None → no cycle"
                ],
                "solution": """def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next          # moves 1 step
        fast = fast.next.next     # moves 2 steps
        if slow == fast:
            return True           # they met → cycle exists
    return False"""
            }
        ]
    },
    "trees": {
        "easy": [
            {
                "id": "tree_e1",
                "title": "Maximum Depth of Binary Tree",
                "problem": """Given the root of a binary tree, return its maximum depth.
Maximum depth is the number of nodes along the longest path from root to leaf.
 
Example 1:
  Input:  root = [3,9,20,null,null,15,7]
  Output: 3
 
Example 2:
  Input:  root = [1,null,2]
  Output: 2
 
Constraints:
  - Number of nodes: 0 to 10^4
  - -100 <= Node.val <= 100""",
                "approach": "DFS: depth = 1 + max(left_depth, right_depth)",
                "time_complexity": "O(n)",
                "space_complexity": "O(h) where h = tree height",
                "companies": ["TCS", "Wipro", "Infosys"],
                "hints": [
                    "Think recursively: depth of a node = 1 + max depth of its subtrees",
                    "Base case: None node has depth 0",
                    "Can also do BFS and count levels"
                ],
                "solution": """def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
 
# BFS approach:
from collections import deque
def max_depth_bfs(root):
    if not root: return 0
    queue, depth = deque([root]), 0
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
    return depth"""
            }
        ]
    },
    "dynamic_programming": {
        "easy": [
            {
                "id": "dp_e1",
                "title": "Climbing Stairs",
                "problem": """You are climbing a staircase. It takes n steps to reach the top.
Each time you can either climb 1 or 2 steps.
In how many distinct ways can you climb to the top?
 
Example 1:
  Input:  n = 2
  Output: 2
  Explanation: Two ways — (1+1) or (2)
 
Example 2:
  Input:  n = 3
  Output: 3
  Explanation: Three ways — (1+1+1), (1+2), (2+1)
 
Constraints:
  - 1 <= n <= 45""",
                "approach": "DP: ways(n) = ways(n-1) + ways(n-2) — this is Fibonacci!",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "companies": ["Amazon", "TCS", "Infosys"],
                "hints": [
                    "To reach step n, you came from step n-1 (1 step) or step n-2 (2 steps)",
                    "So ways(n) = ways(n-1) + ways(n-2) — recognize this pattern?",
                    "This is exactly the Fibonacci sequence! Base cases: ways(1)=1, ways(2)=2"
                ],
                "solution": """def climb_stairs(n):
    if n <= 2: return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b"""
            }
        ],
        "medium": [
            {
                "id": "dp_m1",
                "title": "Longest Common Subsequence (LCS)",
                "problem": """Given two strings text1 and text2, return the length of their longest common subsequence.
A subsequence is a sequence that appears in the same relative order but not necessarily contiguous.
 
Example 1:
  Input:  text1 = "abcde", text2 = "ace"
  Output: 3
  Explanation: LCS is "ace"
 
Example 2:
  Input:  text1 = "abc", text2 = "abc"
  Output: 3
 
Example 3:
  Input:  text1 = "abc", text2 = "def"
  Output: 0
 
Constraints:
  - 1 <= text1.length, text2.length <= 1000""",
                "approach": "2D DP: dp[i][j] = LCS length of text1[:i] and text2[:j]",
                "time_complexity": "O(m × n)",
                "space_complexity": "O(m × n)",
                "companies": ["Google", "Adobe", "Flipkart"],
                "hints": [
                    "Build a 2D table where dp[i][j] = LCS of first i chars of text1 and first j chars of text2",
                    "If text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1",
                    "Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])"
                ],
                "solution": """def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]"""
            }
        ]
    },
    "graphs": {
        "medium": [
            {
                "id": "graph_m1",
                "title": "Number of Islands",
                "problem": """Given an m x n 2D binary grid where '1' represents land and '0' represents water,
return the number of islands.
An island is surrounded by water and formed by connecting adjacent lands horizontally or vertically.
 
Example 1:
  Input:
    grid = [
      ["1","1","1","1","0"],
      ["1","1","0","1","0"],
      ["1","1","0","0","0"],
      ["0","0","0","0","0"]
    ]
  Output: 1
 
Example 2:
  Input:
    grid = [
      ["1","1","0","0","0"],
      ["1","1","0","0","0"],
      ["0","0","1","0","0"],
      ["0","0","0","1","1"]
    ]
  Output: 3
 
Constraints:
  - m == grid.length, n == grid[i].length
  - 1 <= m, n <= 300""",
                "approach": "DFS/BFS: for each unvisited '1', do DFS to mark entire island",
                "time_complexity": "O(m × n)",
                "space_complexity": "O(m × n) recursion stack",
                "companies": ["Amazon", "Google", "Microsoft"],
                "hints": [
                    "When you find a '1', that's a new island — increment count",
                    "Then use DFS to visit all connected '1's and mark them as visited ('0')",
                    "Repeat until entire grid is scanned"
                ],
                "solution": """def num_islands(grid):
    if not grid: return 0
    count = 0
    def dfs(r, c):
        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]) or grid[r][c] != '1':
            return
        grid[r][c] = '0'  # mark as visited
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count"""
            }
        ]
    },
    "sorting": {
        "easy": [
            {
                "id": "sort_e1",
                "title": "Merge Sorted Arrays",
                "problem": """You are given two integer arrays nums1 and nums2, sorted in non-decreasing order,
and two integers m and n, representing the number of elements in nums1 and nums2 respectively.
Merge nums2 into nums1 in-place so that nums1 becomes sorted.
 
Note: nums1 has length m + n, with the last n elements set to 0 as placeholders.
 
Example 1:
  Input:  nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
  Output: [1,2,2,3,5,6]
 
Example 2:
  Input:  nums1 = [1], m = 1, nums2 = [], n = 0
  Output: [1]
 
Constraints:
  - nums1.length == m + n
  - 0 <= m, n <= 200""",
                "approach": "Two pointers from the END — fill from back to avoid overwriting",
                "time_complexity": "O(m + n)",
                "space_complexity": "O(1)",
                "companies": ["TCS", "Infosys", "Microsoft"],
                "hints": [
                    "Filling from the front would overwrite elements. Fill from the BACK instead",
                    "Use three pointers: p1=m-1, p2=n-1, p=m+n-1 (write position)",
                    "Compare nums1[p1] vs nums2[p2], place the larger at nums1[p]"
                ],
                "solution": """def merge(nums1, m, nums2, n):
    p1, p2, p = m - 1, n - 1, m + n - 1
    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1
    # Copy remaining from nums2 (if any)
    nums1[:p2+1] = nums2[:p2+1]"""
            }
        ]
    }
}