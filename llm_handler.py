# llm_handler.py
import os
import json
import re
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import prompts

load_dotenv()

# Pre-packaged high-quality mock database for realistic Mock Mode
MOCK_DATABASE = {
    "Software Development Engineer (SDE)": {
        "Easy": [
            {
                "id": 1,
                "question": "Explain the difference between an Array and a Linked List. When would you use one over the other?",
                "expected_topics": ["Contiguous memory", "Pointers/Nodes", "Index-based access time complexity", "Insertion/Deletion at head"],
                "hint": "Think about how they are stored in memory. How does searching for an element by index compare to inserting a new element at the very beginning?",
                "follow_up_question": "You mentioned arrays have contiguous memory. How does dynamic resizing work for arrays (like ArrayList in Java or lists in Python), and what is its amortized time complexity?",
                "follow_up_hint": "Think about what happens when the array capacity is reached and we need to add another element. How much memory is allocated and what operation is performed?",
                "mock_evaluation": {
                    "score": 8,
                    "correctness_feedback": "Excellent explanation of the contiguous memory structure of arrays vs. pointer-linked nodes of lists. Correctly identified O(1) random access for arrays and O(1) insertion for linked lists.",
                    "communication_feedback": "Very clear structure. Using terms like 'random access' and 'pointer overhead' demonstrates strong technical vocabulary.",
                    "strengths": ["Clear breakdown of memory layout differences", "Correct Big-O time complexity analysis for basic operations"],
                    "improvement_tips": ["Mention the cache locality benefits of arrays due to contiguous memory allocation."]
                },
                "mock_follow_up_evaluation": {
                    "score": 9,
                    "correctness_feedback": "Spot-on! Explaining the doubling mechanism and the O(1) amortized insertion cost shows you understand the details of dynamic sizing.",
                    "communication_feedback": "Concise and precise. Highlighting the distinction between worst-case and amortized costs is very professional.",
                    "strengths": ["Accurate definition of amortized complexity", "Correct description of array doubling and copying"],
                    "improvement_tips": ["Mention that shrinking the array is typically not done automatically, or explain the threshold at which some implementations shrink it."]
                }
            },
            {
                "id": 2,
                "question": "What is the difference between a Process and a Thread in operating systems?",
                "expected_topics": ["Address space", "Memory sharing", "Context switching overhead", "IPC (Inter-Process Communication)"],
                "hint": "Think about which one owns the resources and address space, and how they communicate with each other.",
                "follow_up_question": "Since threads share the same memory space, what issues can arise, and how can we prevent them?",
                "follow_up_hint": "Think about what happens when two threads try to write to the same variable simultaneously. What synchronization primitives can we use?",
                "mock_evaluation": {
                    "score": 7,
                    "correctness_feedback": "Good job. You correctly identified that a process is an isolated executing program with its own memory space, whereas threads are units of execution within a process that share memory.",
                    "communication_feedback": "Easy to follow. Adding a real-world example of a process (like a browser) and threads (like tabs or background downloading) would make it even stronger.",
                    "strengths": ["Correctly identified memory sharing behavior", "Explained resource isolation boundaries well"],
                    "improvement_tips": ["Mention that context switching between threads is faster than between processes because page tables don't need to be swapped."]
                },
                "mock_follow_up_evaluation": {
                    "score": 8,
                    "correctness_feedback": "Nice. You discussed race conditions and data corruption, and correctly mentioned Mutexes, Locks, and Semaphores as solutions.",
                    "communication_feedback": "Clear explanation of thread safety concepts.",
                    "strengths": ["Defined race conditions accurately", "Identified standard synchronization mechanisms"],
                    "improvement_tips": ["Briefly mention the risk of deadlocks when using multiple locks, as it is a common follow-up topic."]
                }
            },
            {
                "id": 3,
                "question": "Explain the concept of Recursion and how the Call Stack is used during recursive execution.",
                "expected_topics": ["Base case", "Recursive step", "Stack Overflow", "Stack frame activation records"],
                "hint": "Think about what prevents a recursive function from calling itself infinitely, and where the local variables and return addresses are stored.",
                "follow_up_question": "What is Tail Recursion, and how do compilers optimize it?",
                "follow_up_hint": "Think about a recursive call that is the absolute last operation in the function. Does the compiler still need to keep the current stack frame?",
                "mock_evaluation": {
                    "score": 8,
                    "correctness_feedback": "Great overview of recursion. You clearly defined the base case and the recursive step, and explained stack frame pushing and popping accurately.",
                    "communication_feedback": "Structured, logical explanation.",
                    "strengths": ["Excellent definition of base case necessity", "Clear explanation of stack overflow causes"],
                    "improvement_tips": ["Give a quick example of a function call stack trace (e.g. factorial(3)) to show exactly how frames build up and unwind."]
                },
                "mock_follow_up_evaluation": {
                    "score": 7,
                    "correctness_feedback": "You correctly described tail recursion as a call at the end of the function. For optimization, tail call optimization (TCO) reuses the current stack frame instead of creating a new one, reducing space complexity to O(1).",
                    "communication_feedback": "Good explanation, but could be slightly more precise on how frame reuse works.",
                    "strengths": ["Defined tail recursive structures correctly", "Stated O(1) space complexity benefit"],
                    "improvement_tips": ["Mention that not all languages support tail call optimization (for instance, Python does not, whereas Scala or Haskell do)."]
                }
            }
        ],
        "Medium": [
            {
                "id": 1,
                "question": "Design a URL Shortening service (like bit.ly). What are the key database requirements and how would you generate unique short aliases?",
                "expected_topics": ["Base 62 encoding", "MD5/SHA-256 hashing", "Distributed Counter / Range Handler", "Write/Read ratios & caching (Redis)"],
                "hint": "Consider how many unique URLs you need to support and what characters can be used in the shortened URL. How can you map a long URL to a short alphanumeric key?",
                "follow_up_question": "If our system needs to scale to handle 10,000 read requests per second and only 100 write requests per second, how would you optimize the read path?",
                "follow_up_hint": "With a high read-to-write ratio, look into caching layers and database replication. Which cache eviction policy would you use?",
                "mock_evaluation": {
                    "score": 8,
                    "correctness_feedback": "Excellent database and encoding choices. You correctly selected Base62 encoding to generate short aliases. Your choice of a relational database with indexing or a key-value store was sound.",
                    "communication_feedback": "Very structured. Discussing scaling numbers and system constraints upfront is a senior engineering habit.",
                    "strengths": ["Great estimation of character spacing (Base62)", "Good architectural breakdown of app server and database"],
                    "improvement_tips": ["Explain how you handle hash collisions if you use MD5/SHA-256 (e.g. appending a counter or checking DB)."]
                },
                "mock_follow_up_evaluation": {
                    "score": 9,
                    "correctness_feedback": "Spot on. Utilizing a caching layer like Redis (with LRU eviction) and read replicas for the database will easily handle the 10,000 reads/sec. Correctly pointed out that caching works extremely well because URL redirection has high read locality.",
                    "communication_feedback": "Crisp and architectural.",
                    "strengths": ["Excellent use of Redis/Memcached cache layer", "Good application of DB read replicas and cache policies"],
                    "improvement_tips": ["Discuss CDN usage for geographic distribution of redirect routing if the system is global."]
                }
            }
        ],
        "Hard": [
            {
                "id": 1,
                "question": "How would you design a distributed rate limiter for an API that handles 100M daily active users? Compare the Token Bucket and Sliding Window Log algorithms.",
                "expected_topics": ["Token Bucket", "Sliding Window Log", "Redis cluster (sorted sets)", "Race conditions & atomic operations (Lua scripts)", "Distributed latency"],
                "hint": "Think about memory constraints per user and accuracy. Token Bucket is memory efficient, whereas Sliding Window Log records every timestamp. How do we sync this across multiple servers?",
                "follow_up_question": "How would you handle race conditions in Redis when two concurrent requests from the same user arrive at different application servers at the exact same millisecond?",
                "follow_up_hint": "Redis is single-threaded, but read-then-write operations are not atomic. What Redis feature allows executing multiple commands atomically?",
                "mock_evaluation": {
                    "score": 8,
                    "correctness_feedback": "Outstanding comparison. You accurately detailed the memory footprint of Sliding Window (storing all timestamps) versus Token Bucket (storing just token count and last timestamp).",
                    "communication_feedback": "Highly professional, clear separation of algorithm properties.",
                    "strengths": ["Clear tradeoffs on memory and accuracy", "Solid understanding of distributed architecture layers"],
                    "improvement_tips": ["Mention Sliding Window Counter as a hybrid approach that reduces memory while avoiding boundary resets."]
                },
                "mock_follow_up_evaluation": {
                    "score": 9,
                    "correctness_feedback": "Great response. Using Redis Lua scripts to execute the rate limiter check-and-decrement atomically is the industry standard. This prevents concurrent race conditions because Redis executes the script in a single block.",
                    "communication_feedback": "Strong systems engineering terminology.",
                    "strengths": ["Correct identification of Redis Lua script atomicity", "Recognized read-modify-write race conditions"],
                    "improvement_tips": ["Briefly mention Redis locks or Redlock if we had to coordinate across multiple distinct Redis nodes (though local scripting is usually enough for a single cluster)."]
                }
            }
        ]
    },
    "Machine Learning Engineer (ML)": {
        "Easy": [
            {
                "id": 1,
                "question": "What is the Bias-Variance trade-off? How do overfitting and underfitting relate to these concepts?",
                "expected_topics": ["High bias = Underfitting", "High variance = Overfitting", "Generalization error", "Model complexity"],
                "hint": "Recall what bias and variance measure in terms of training versus validation errors, and how model complexity affects them.",
                "follow_up_question": "If your model is suffering from high variance, what are 3 specific techniques you would use to address this?",
                "follow_up_hint": "High variance means the model is overfitting. Think about data, model structure, and training constraints.",
                "mock_evaluation": {
                    "score": 8,
                    "correctness_feedback": "Very accurate definition. Bias is the error from erroneous assumptions in the model. Variance is the error from sensitivity to small fluctuations in the training set. Correctly mapped them to underfitting/overfitting.",
                    "communication_feedback": "Structured, easy to read. Visualizing the bullseye target model is a great mental frame.",
                    "strengths": ["Perfect mapping of error types to fitting states", "Clear explanation of model complexity curves"],
                    "improvement_tips": ["Mention the mathematical decomposition of mean squared error (MSE) into bias^2 + variance + irreducible noise."]
                },
                "mock_follow_up_evaluation": {
                    "score": 8,
                    "correctness_feedback": "Good. You listed regularisation (L1/L2), gathering more training data, and reducing model complexity (or using pruning/dropout) which are classic remedies for overfitting.",
                    "communication_feedback": "Clear bullet points.",
                    "strengths": ["Identified standard regularization paths", "Explained why more data helps generalize"],
                    "improvement_tips": ["Mention early stopping or cross-validation as essential tools to monitor variance during training."]
                }
            }
        ],
        "Medium": [
            {
                "id": 1,
                "question": "Explain the difference between L1 (Lasso) and L2 (Ridge) regularization. Why does L1 regularization lead to sparse weights?",
                "expected_topics": ["Absolute weights vs Squared weights", "Feature selection", "Geometric explanation (diamond vs circle intersections)", "Gradient at zero"],
                "hint": "Think about the shape of the constraint regions. Why does the L1 norm constraint encourage optimal weights to sit on the coordinate axes?",
                "follow_up_question": "If you have a dataset with highly correlated features, how do L1 and L2 regularization behave differently, and which one would you prefer?",
                "follow_up_hint": "If features A and B are identical, L1 will pick one randomly and set the other to 0. What does L2 do to their weights?",
                "mock_evaluation": {
                    "score": 8,
                    "correctness_feedback": "Great explanation. You described L1 as adding the absolute values of weights to the loss, and L2 as adding the squared values. The explanation of why L1 forces weights to zero (due to the sharp corners of the L1 diamond contour) was solid.",
                    "communication_feedback": "Excellent technical articulation. Geometric intuition is very helpful here.",
                    "strengths": ["Correct math definitions", "Good geometric intuition for sparsity"],
                    "improvement_tips": ["Briefly mention ElasticNet, which combines both L1 and L2 to get the benefits of feature selection and correlated grouping."]
                },
                "mock_follow_up_evaluation": {
                    "score": 9,
                    "correctness_feedback": "Perfect response. Under highly correlated features, L1 will arbitrarily pick one feature and zero the others, which can make model interpretation unstable. L2 will distribute the weights roughly equally among them. Hence, ElasticNet or L2 is preferred for correlated feature groups.",
                    "communication_feedback": "Extremely clear, showing deep conceptual understanding.",
                    "strengths": ["Accurate depiction of correlated feature handling", "Good recommendation of ElasticNet/L2"],
                    "improvement_tips": ["Explain how this affects feature importance interpretation in production environments."]
                }
            }
        ],
        "Hard": [
            {
                "id": 1,
                "question": "Describe the architecture and self-attention mechanism of the Transformer model. Why does it scale better than LSTMs?",
                "expected_topics": ["Queries, Keys, and Values", "Scaled Dot-Product Attention", "Parallelization vs Sequential processing", "Multi-Head Attention", "O(N^2) complexity vs O(N) step dependence"],
                "hint": "Compare how LSTMs process tokens step-by-step (sequentially) with how Transformers process all tokens simultaneously (parallelized). What role do Query, Key, and Value matrices play?",
                "follow_up_question": "What is the time and space complexity of standard self-attention with respect to sequence length N, and how do modern architectures (like FlashAttention) optimize this?",
                "follow_up_hint": "Self-attention computes an N x N matrix. FlashAttention optimizes this by avoiding writing the large attention matrix to slow GPU memory. Think about hardware memory bounds.",
                "mock_evaluation": {
                    "score": 8,
                    "correctness_feedback": "Excellent explanation of Query, Key, Value mappings and the self-attention formula. You correctly identified parallel processing as the main factor enabling Transformers to scale compared to sequential LSTMs.",
                    "communication_feedback": "Professional explanation. Using standard mathematical terms (softmax, dot-product scaling) correctly.",
                    "strengths": ["Clear breakdown of sequential vs. parallel training", "Solid understanding of Q, K, V mathematical interaction"],
                    "improvement_tips": ["Explicitly mention positional encodings, since self-attention alone is permutation-invariant and has no notion of word order."]
                },
                "mock_follow_up_evaluation": {
                    "score": 9,
                    "correctness_feedback": "Superb answer. Standard attention is indeed O(N^2) in both time and space. You correctly explained that FlashAttention is an IO-aware algorithm that computes softmax in blocks (using tiling) without writing the huge N x N matrix back to High Bandwidth Memory (HBM), keeping SRAM usage optimized.",
                    "communication_feedback": "Exceptional depth. Explaining hardware-level memory layers (HBM vs SRAM) is outstanding for ML infrastructure rounds.",
                    "strengths": ["Correct O(N^2) complexity analysis", "Excellent technical description of FlashAttention block tiling and IO optimization"],
                    "improvement_tips": ["Mention other linear attention approximations like Linformer or sliding window attention (Mistral) as alternative sequence length remedies."]
                }
            }
        ]
    },
    "Data Analyst": {
        "Easy": [
            {
                "id": 1,
                "question": "What is the difference between INNER JOIN, LEFT JOIN, and FULL OUTER JOIN in SQL? Give an example scenario for each.",
                "expected_topics": ["Matching rows", "Null values for missing matches", "All rows from both tables", "SQL query examples"],
                "hint": "Think about a table of Customers and a table of Orders. What happens when a customer has no orders, or an order has no valid customer ID?",
                "follow_up_question": "Suppose you run a LEFT JOIN and notice that some rows have NULL values in the right table's columns. How would you handle or replace these NULL values in your final report?",
                "follow_up_hint": "Look into standard SQL functions like COALESCE, IFNULL, or CASE WHEN statements to provide default values.",
                "mock_evaluation": {
                    "score": 8,
                    "correctness_feedback": "Clear explanation of table joins. The examples of Customers and Orders are perfect for explaining the differences in row outputs and NULL handling.",
                    "communication_feedback": "Well-structured. Using visual representations (like Venn diagrams or tabular results) in description helps a lot.",
                    "strengths": ["Excellent scenario examples", "Correct description of JOIN matching logic"],
                    "improvement_tips": ["Briefly mention performance: INNER JOINs can be optimized faster than LEFT/FULL JOINs because the database engine has more freedom to filter rows early."]
                },
                "mock_follow_up_evaluation": {
                    "score": 8,
                    "correctness_feedback": "Good job. Using `COALESCE(column, default_value)` or a `CASE` expression are the ideal ways to clean NULL values in SQL queries.",
                    "communication_feedback": "Short and accurate response.",
                    "strengths": ["Used standard SQL function COALESCE", "Understands report data-cleaning principles"],
                    "improvement_tips": ["Explain when you might want to filter out NULLs altogether vs. when keeping and replacing them is required for summary statistics (like count/average)."]
                }
            }
        ],
        "Medium": [
            {
                "id": 1,
                "question": "What is A/B testing? How do you determine if the difference in conversion rate between two groups is statistically significant?",
                "expected_topics": ["Hypothesis testing", "Null Hypothesis (H0)", "P-value & Alpha threshold", "Z-test or T-test", "Statistical power & Sample size"],
                "hint": "Recall what a Null Hypothesis is. How does a p-value help you decide whether to reject or fail to reject the null hypothesis?",
                "follow_up_question": "What is the 'Multiple Comparisons Problem' (or look-elsewhere effect) in A/B testing, and how does it affect your Type I error rate? How would you fix it?",
                "follow_up_hint": "If you test 20 different metrics at a 95% confidence level, what is the probability of finding a false positive? Think about Bonferroni correction.",
                "mock_evaluation": {
                    "score": 7,
                    "correctness_feedback": "Good. You correctly defined control vs. treatment, formulated H0/H1, and explained that p-value < 0.05 is the typical threshold for significance.",
                    "communication_feedback": "Clear language, avoiding overly complex math speak where plain definitions suffice.",
                    "strengths": ["Accurate definition of Null Hypothesis", "Understands p-value decision criteria"],
                    "improvement_tips": ["Mention that sample size calculation (power analysis) must be done *before* starting the test to ensure the experiment is powered to detect the minimum detectable effect (MDE)."]
                },
                "mock_follow_up_evaluation": {
                    "score": 9,
                    "correctness_feedback": "Excellent answer. Testing multiple metrics increases the probability of Type I error (false positives). You correctly identified the Bonferroni correction (adjusting alpha to alpha/k) or FDR controls (Benjamini-Hochberg) as the appropriate solutions.",
                    "communication_feedback": "Very professional and statistically rigorous.",
                    "strengths": ["Correct calculation of cumulative false positive risk", "Accurately proposed Bonferroni adjustment"],
                    "improvement_tips": ["Explain the tradeoff: Bonferroni is highly conservative and can drastically increase Type II error (false negatives), so sometimes holm-bonferroni or FDR is preferred in product analytics."]
                }
            }
        ],
        "Hard": [
            {
                "id": 1,
                "question": "Explain the concept of Cohort Analysis. How would you write a SQL query to calculate user retention rate month-over-month?",
                "expected_topics": ["Group by signup month", "Self-join on user_id", "Datediff/date_trunc", "Aggregation with conditional count", "Pivot / cohort grid representation"],
                "hint": "You need to identify a cohort (e.g. users signed up in a specific month) and track their activity in subsequent months. Start by joining your user signup table with their activity transactions table.",
                "follow_up_question": "How do you distinguish between a cohort retention drop due to poor product onboarding versus poor long-term product-market fit? How would you visualize this in a retention curve?",
                "follow_up_hint": "Onboarding issues affect the first few periods (steep drop at the beginning). Product-market fit issues cause the retention curve to continuously decline instead of flattening out. What shape should a healthy retention curve have?",
                "mock_evaluation": {
                    "score": 8,
                    "correctness_feedback": "Strong explanation. You laid out the SQL logic correctly: first CTE to get signup date, second CTE to get active months per user, and joining them to calculate the monthly delta.",
                    "communication_feedback": "Clean logic breakdown. Writing pseudo-SQL or explaining CTE flow makes it easy for interviewers to follow.",
                    "strengths": ["Correct SQL join logic for cohorts", "Clear explanation of cohort tracking metrics"],
                    "improvement_tips": ["Provide an example retention table layout (Cohort, Month 0, Month 1, Month 2...) to show how the final output is formatted."]
                },
                "mock_follow_up_evaluation": {
                    "score": 9,
                    "correctness_feedback": "Perfect analysis. Onboarding failure results in a sharp drop in Month 1/2, but if the curve flattens out afterwards, the remaining users are loyal (indicating product-market fit). If the curve never flattens and trends to zero, there is a lack of PMF. Visualized as a line chart, a flat tail is the goal.",
                    "communication_feedback": "Excellent business and analytical reasoning. Highly structured.",
                    "strengths": ["Correctly interpreted curve flattening", "Clear distinction between onboarding drop vs. churn slope"],
                    "improvement_tips": ["Mention that cohort segmentation (e.g., by traffic channel or feature usage) can pinpoint *why* certain cohorts flatten out higher than others."]
                }
            }
        ]
    }
}


class LLMHandler:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.llm = None
        self.mock_mode = True
        
        if self.api_key:
            try:
                # Initialize ChatGroq
                self.llm = ChatGroq(
                    model="llama-3.3-70b-versatile",
                    groq_api_key=self.api_key,
                    temperature=0.7
                )
                self.mock_mode = False
            except Exception as e:
                # If LLaMA 3.3 fails or isn't available, try LLaMA 3 70B
                try:
                    self.llm = ChatGroq(
                        model="llama3-70b-8192",
                        groq_api_key=self.api_key,
                        temperature=0.7
                    )
                    self.mock_mode = False
                except Exception as ex:
                    print(f"Error initializing ChatGroq: {ex}. Falling back to Mock Mode.")
                    self.mock_mode = True
        else:
            print("No GROQ_API_KEY provided. Operating in Mock Mode.")
            self.mock_mode = True

    def is_mock_mode(self):
        return self.mock_mode

    def generate_questions(self, role, difficulty, topic, num_questions=3):
        """Generates domain-specific technical questions."""
        if self.mock_mode:
            # Retrieve from mock database
            role_data = MOCK_DATABASE.get(role, MOCK_DATABASE["Software Development Engineer (SDE)"])
            diff_data = role_data.get(difficulty, role_data["Easy"])
            
            # Return up to num_questions questions
            questions = []
            for i, item in enumerate(diff_data[:num_questions]):
                questions.append({
                    "id": item["id"],
                    "question": item["question"],
                    "expected_topics": item["expected_topics"]
                })
            
            # If we don't have enough, pad it with generic ones
            while len(questions) < num_questions:
                pad_id = len(questions) + 1
                questions.append({
                    "id": pad_id,
                    "question": f"Provide an example of a challenging {topic} problem you faced and how you resolved it in a {role} context.",
                    "expected_topics": ["Problem-solving", "Trade-offs", "Resolution"]
                })
            return questions

        # Call Groq LLM
        prompt = ChatPromptTemplate.from_messages([
            ("system", prompts.QUESTION_GENERATOR_SYSTEM),
            ("user", "Please generate the questions now.")
        ])
        
        chain = prompt | self.llm
        try:
            response = chain.invoke({
                "role": role,
                "difficulty": difficulty,
                "topic": topic,
                "num_questions": num_questions
            })
            text = response.content.strip()
            
            # Try to extract JSON from response text (handling code blocks)
            json_match = re.search(r'\[\s*\{.*\}\s*\]', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            return json.loads(text)
        except Exception as e:
            print(f"Failed to generate questions via LLM: {e}. Falling back to Mock Mode.")
            # Temporary switch to mock database to prevent crash
            self.mock_mode = True
            res = self.generate_questions(role, difficulty, topic, num_questions)
            self.mock_mode = False # Keep LLM active for other queries if possible
            return res

    def get_hint(self, role, difficulty, question, answer_so_far="", question_id=1, is_follow_up=False):
        """Generates a hint for the current question."""
        if self.mock_mode:
            role_data = MOCK_DATABASE.get(role, MOCK_DATABASE["Software Development Engineer (SDE)"])
            diff_data = role_data.get(difficulty, role_data["Easy"])
            # Match by question text similarity or ID
            for item in diff_data:
                if item["id"] == question_id or question[:15] in item["question"]:
                    return item["follow_up_hint"] if is_follow_up else item["hint"]
            return "Consider the fundamental constraints, performance bottlenecks, or trade-offs of the technologies involved."

        prompt = ChatPromptTemplate.from_messages([
            ("system", prompts.HINT_SYSTEM),
            ("user", "Question: {question}\nCandidate's response so far: {answer_so_far}\nPlease provide the hint.")
        ])
        
        chain = prompt | self.llm
        try:
            response = chain.invoke({
                "question": question,
                "answer_so_far": answer_so_far
            })
            return response.content.strip()
        except Exception as e:
            print(f"Failed to get hint: {e}")
            return "Think about the efficiency of your approach, potential edge cases, and the underlying data structures/mechanisms."

    def evaluate_answer(self, role, difficulty, question, user_answer, question_id=1, is_follow_up=False):
        """Evaluates candidate's response and returns structured feedback."""
        if self.mock_mode:
            role_data = MOCK_DATABASE.get(role, MOCK_DATABASE["Software Development Engineer (SDE)"])
            diff_data = role_data.get(difficulty, role_data["Easy"])
            
            mock_eval = None
            for item in diff_data:
                if item["id"] == question_id or question[:15] in item["question"]:
                    mock_eval = item["mock_follow_up_evaluation"] if is_follow_up else item["mock_evaluation"]
                    break
            
            if not mock_eval:
                # Default generic mock evaluation
                word_count = len(user_answer.split())
                score = min(10, max(2, int(word_count / 12) + 3))
                mock_eval = {
                    "score": score,
                    "correctness_feedback": "Your response contains good keywords but lacks a deep technical explanation. Try outlining your step-by-step approach.",
                    "communication_feedback": "Structure is clear, but consider explaining the 'why' behind your technical choices to show leadership.",
                    "strengths": ["Addresses the topic directly", "Demonstrates basic awareness of the concepts"],
                    "improvement_tips": ["Provide a concrete code or design pattern example.", "Elaborate on operational complexity."]
                }
            return mock_eval

        prompt = ChatPromptTemplate.from_messages([
            ("system", prompts.EVALUATION_SYSTEM),
            ("user", "Evaluate the candidate's answer now.")
        ])
        
        chain = prompt | self.llm
        try:
            response = chain.invoke({
                "question": question,
                "user_answer": user_answer,
                "role": role,
                "difficulty": difficulty
            })
            text = response.content.strip()
            
            # Extract JSON from response text
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            return json.loads(text)
        except Exception as e:
            print(f"Failed to evaluate answer via LLM: {e}")
            # Generate a dynamic fallback dictionary
            word_count = len(user_answer.split())
            score = min(10, max(4, int(word_count / 15) + 3))
            return {
                "score": score,
                "correctness_feedback": "The LLM could not parse structured evaluation, but your answer shows good effort. (Evaluation Fallback)",
                "communication_feedback": "Communication was fine. Make sure to structure answers with distinct paragraphs.",
                "strengths": ["Responded to the prompt", "Identified core keywords"],
                "improvement_tips": ["Ensure your answer provides specific architectural details.", "State Big-O time and space complexity where relevant."]
            }

    def generate_follow_up(self, role, difficulty, question, user_answer, question_id=1):
        """Generates a contextual follow-up question."""
        if self.mock_mode:
            role_data = MOCK_DATABASE.get(role, MOCK_DATABASE["Software Development Engineer (SDE)"])
            diff_data = role_data.get(difficulty, role_data["Easy"])
            for item in diff_data:
                if item["id"] == question_id or question[:15] in item["question"]:
                    return item["follow_up_question"]
            return f"That is a good starting point. Can you explain the main trade-offs or performance limitations of this choice?"

        prompt = ChatPromptTemplate.from_messages([
            ("system", prompts.FOLLOW_UP_SYSTEM),
            ("user", "Generate the follow-up question now.")
        ])
        
        chain = prompt | self.llm
        try:
            response = chain.invoke({
                "question": question,
                "user_answer": user_answer
            })
            return response.content.strip()
        except Exception as e:
            print(f"Failed to generate follow-up: {e}")
            return "Interesting. Can you describe the potential performance impact or bottlenecks if this system scaled to millions of users?"

    def _compile_local_summary(self, role, difficulty, topic, transcript_list, api_failed=False):
        """Compiles a rich, formatted markdown report locally from the session evaluation transcript."""
        scores = []
        all_strengths = []
        all_improvements = []
        
        for entry in transcript_list:
            if "score" in entry and entry["score"] is not None:
                scores.append(entry["score"])
            if "follow_up_score" in entry and entry["follow_up_score"] is not None and entry["follow_up_score"] > 0:
                scores.append(entry["follow_up_score"])
            if "strengths" in entry and entry["strengths"]:
                all_strengths.extend(entry["strengths"])
            if "improvement_tips" in entry and entry["improvement_tips"]:
                all_improvements.extend(entry["improvement_tips"])
            if "follow_up_strengths" in entry and entry["follow_up_strengths"]:
                all_strengths.extend(entry["follow_up_strengths"])
            if "follow_up_improvement_tips" in entry and entry["follow_up_improvement_tips"]:
                all_improvements.extend(entry["follow_up_improvement_tips"])
                
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0
        
        if avg_score >= 8.5:
            verdict = "🏆 Distinguished / Strong Hire"
        elif avg_score >= 7.0:
            verdict = "✅ Hire"
        elif avg_score >= 5.0:
            verdict = "⚠️ Borderline / Needs Practice"
        else:
            verdict = "❌ No Hire / Needs Substantial Practice"
            
        # Deduplicate strengths and improvements
        all_strengths = list(dict.fromkeys(all_strengths))
        all_improvements = list(dict.fromkeys(all_improvements))
        
        if not all_strengths:
            all_strengths = ["Showed effort in responding to all technical questions", "Engaged with follow-up prompts"]
        if not all_improvements:
            all_improvements = ["Provide more specific details in code/design responses", "Explain architectural trade-offs explicitly"]
            
        summary = f"""# 📊 Session Summary Report
"""
        if api_failed:
            summary += "> [!NOTE]\n> **Recruiter Note:** The live LLM summary compiler encountered a connection timeout. The report below has been compiled locally from your real-time session evaluation data.\n\n"
            
        summary += f"""## Executive Summary
You completed a mock technical interview for the **{role}** role focusing on **{topic}** (Difficulty: **{difficulty}**). 
Based on the real-time feedback gathered during your session, the system has aggregated your scores and compiled this roadmap.

## 📈 Overall Performance Metrics
* **Average Score:** `{avg_score} / 10`
* **Recruiter Verdict:** **{verdict}**

### Session Q&A Breakdown
| Question | Phase | Score | Feedback Summary |
|---|---|---|---|
"""
        for i, entry in enumerate(transcript_list):
            main_fb = entry.get("feedback", "N/A").replace('\n', ' ').replace('|', ' ')
            if "Communication:" in main_fb:
                main_fb = main_fb.split("Communication:")[0].replace("Correctness:", "").strip()
            if len(main_fb) > 120:
                main_fb = main_fb[:117] + "..."
            summary += f"| Q{i+1} Main | Core | `{entry.get('score', 0)}/10` | {main_fb} |\n"
            if entry.get("follow_up_question") and entry.get("follow_up_answer") != "[Skipped]":
                fu_fb = entry.get("follow_up_feedback", "N/A").replace('\n', ' ').replace('|', ' ')
                if "Communication:" in fu_fb:
                    fu_fb = fu_fb.split("Communication:")[0].replace("Correctness:", "").strip()
                if len(fu_fb) > 120:
                    fu_fb = fu_fb[:117] + "..."
                summary += f"| Q{i+1} Follow-up | Deep-dive | `{entry.get('follow_up_score', 0)}/10` | {fu_fb} |\n"

        summary += f"""
## 🌟 Core Strengths
"""
        for s in all_strengths[:5]:
            summary += f"* **{s}**\n"
            
        summary += f"""
## 🔍 Key Gaps & Areas for Improvement
"""
        for imp in all_improvements[:5]:
            summary += f"* **{imp}**\n"
            
        summary += f"""
## 🛠️ Actionable Roadmap
1. 📚 **Review Key Concepts:** Deep dive into: {", ".join(all_improvements[:2]) if all_improvements else "core topic areas"}.
2. 💻 **Hands-On Exercises:** Practice coding or design challenges around these concepts.
3. ⏱️ **Time Management:** Standardize your response length to cover both technical definitions and architectural trade-offs within 3-4 minutes.
"""
        return summary

    def generate_session_summary(self, role, difficulty, topic, transcript_list):
        """Generates the overall session report."""
        if self.mock_mode:
            return self._compile_local_summary(role, difficulty, topic, transcript_list, api_failed=False)

        # Format the transcript list into a readable string
        formatted_transcript = ""
        for i, entry in enumerate(transcript_list):
            formatted_transcript += f"### Question {i+1}: {entry['question']}\n"
            formatted_transcript += f"- **Answer**: {entry['answer']}\n"
            formatted_transcript += f"- **Score**: {entry['score']}/10\n"
            formatted_transcript += f"- **Feedback**: {entry['feedback']}\n\n"
            if entry.get("follow_up_question"):
                formatted_transcript += f"  - **Follow-up**: {entry['follow_up_question']}\n"
                formatted_transcript += f"  - **Follow-up Answer**: {entry.get('follow_up_answer', 'N/A')}\n"
                formatted_transcript += f"  - **Follow-up Score**: {entry.get('follow_up_score', 'N/A')}/10\n"
                formatted_transcript += f"  - **Follow-up Feedback**: {entry.get('follow_up_feedback', 'N/A')}\n\n"

        prompt = ChatPromptTemplate.from_messages([
            ("system", prompts.SUMMARY_SYSTEM),
            ("user", "Compile the Session Summary Report now.")
        ])
        
        chain = prompt | self.llm
        try:
            response = chain.invoke({
                "role": role,
                "difficulty": difficulty,
                "topic": topic,
                "transcript": formatted_transcript
            })
            return response.content.strip()
        except Exception as e:
            print(f"Failed to generate session summary: {e}. Compiling locally.")
            return self._compile_local_summary(role, difficulty, topic, transcript_list, api_failed=True)
