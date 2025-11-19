<h1> Loan Transaction Blockchain Simulator</h1>

<p>This project is a web-based simulation of a simple blockchain, implemented using Python (Flask) and a custom <code>Blockchain</code> class. It demonstrates the core principles of blockchain technology, including transaction aggregation, mining, and immutable data storage.</p>

<h2> Features</h2>

<p>The application allows users to interact with the blockchain through a simple web interface, managing the blockchain of <strong>Loan Transactions</strong>.</p>

<h3>Core Blockchain Mechanics</h3>
<ul>
<li><strong>Initialization:</strong> The blockchain starts with a mandatory <strong>Genesis Block</strong> (Index 1), establishing the chain's origin.</li>
<li><strong>Transaction Handling (<code>ADD</code>):</strong> Users can add transactions (Borrower, Lender, Amount) which are placed into a queue of <strong>Pending Transactions</strong>.</li>
<li><strong>Block Creation (<code>MINE</code>):</strong> The mining function packages all pending transactions into a new block, calculates its hash, and permanently adds the block to the chain.</li>
<li><strong>Immutable blockchain:</strong> Block indexing starts at <strong>Index 1</strong> for human-readable tracking.</li>
</ul>

<h3>Web Interface & Visualization</h3>
<ul>
<li><strong>Real-Time Data View:</strong> The interface continuously displays the full blockchain and any pending transactions.</li>
<li><strong>Interactive Block Viewer:</strong> The main chain is displayed using a Bootstrap Accordion. Users can expand any block header to view its full transaction data, timestamp, proof value, and hash reference.</li>
</ul>

<ul>
<li><strong>Export Functionality:</strong> Users can export the entire current blockchain structure as a JSON file for review and archival.</li>
</ul>

<h3>Usability and Aesthetics</h3>
<p>The application features a modern, clean design:</p>
<ul>
<li><strong>Dark Mode:</strong> A global dark gray background (<code>bg-dark</code>) is used throughout the page.</li>
<li><strong>Pale Pink Accents:</strong> Interactive elements, including the <strong>Export button</strong>, <strong>status messages</strong>, and the <strong>active accordion header</strong>, are styled in a custom pale pink (<code>#F8C8DC</code>) for visual consistency and focus.</li>
</ul>

<h2> Getting Started</h2>

<p>These instructions will get you a copy of the project up and running on your local machine.</p>

<h3>Prerequisites</h3>
<p>You need Python 3 installed. This project requires the following Python libraries:</p>

<pre><code>pip install Flask
</code></pre>

<h3>Running the Application</h3>
<ol>
<li>Ensure you have the following files in your project directory:
<ul>
<li><code>main.py</code> (Flask application logic)</li>
<li><code>A4.py</code> (The custom <code>Blockchain</code> class definition)</li>
<li><code>index.html</code> (The web interface template)</li>
</ul>
</li>
<li>Run the Flask application from your terminal:</li>
</ol>

<pre><code>python main.py
</code></pre>

<ol start="3">
<li>Open your web browser and navigate to the local server address specified in <code>main.py</code>).</li>
</ol>

<h2> Usage Guide</h2>

<p>The application supports three main actions:</p>

<table>
<thead>
<tr>
<th>Action</th>
<th>Description</th>
<th>Result</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Add Transaction</strong></td>
<td>Enter a <strong>Borrower</strong>, <strong>Lender</strong>, and <strong>Amount</strong>.</td>
<td>The transaction is placed in the <strong>Pending Transactions</strong> queue.</td>
</tr>
<tr>
<td><strong>Mine Block</strong></td>
<td>Click the <strong>Mine Block</strong> button.</td>
<td>All pending transactions are packaged into a new block and permanently added to the blockchain.</td>
</tr>
<tr>
<td><strong>Export Chain</strong></td>
<td>Click the <strong>Export Chain (JSON)</strong> button.</td>
<td>The entire blockchain is saved and downloaded as a JSON file.</td>
</tr>
</tbody>
</table>

<h2> Technical Stack</h2>
<ul>
<li><strong>Backend:</strong> Python 3, Flask</li>
<li><strong>Frontend:</strong> HTML5, Bootstrap 5 (CSS/JS bundle), Jinja Templating (for rendering data)</li>
<li><strong>Core Logic:</strong> Custom <code>Blockchain</code> class (<code>A4.py</code>) handling all hashing, proof, and data structure rules.</li>
</ul>
