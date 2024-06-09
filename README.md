<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Places Collector</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }
        h1, h2, h3 {
            color: #2C3E50;
        }
        code {
            background-color: #ECF0F1;
            padding: 2px 4px;
            border-radius: 4px;
        }
        pre {
            background-color: #ECF0F1;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
        .button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            outline: none;
            color: #fff;
            background-color: #3498DB;
            border: none;
            border-radius: 15px;
            box-shadow: 0 5px #2980B9;
        }
        .button:hover {
            background-color: #2980B9;
        }
        .button:active {
            background-color: #2980B9;
            box-shadow: 0 5px #1A5276;
            transform: translateY(4px);
        }
    </style>
</head>
<body>

<h1>Google Places Collector</h1>

<p>This project is designed to search for various types of locations using the Google Places API and save the results to an Excel file. Users can choose from a wide range of location types such as real estate, supermarkets, gas stations, restaurants, hospitals, and more. The project is multilingual, supporting both English and Arabic languages.</p>

<h2>Features</h2>
<ul>
    <li>Search for different types of locations using the Google Places API.</li>
    <li>Supports a wide range of location types.</li>
    <li>Multilingual support (English and Arabic).</li>
    <li>Results are saved to an Excel file with clickable WhatsApp links.</li>
</ul>

<h2>Installation</h2>
<pre><code>pip install -r requirements.txt</code></pre>

<h2>Usage</h2>
<p>Run the script using the following command:</p>
<pre><code>python google_places_collector.py</code></pre>

<h3>Step-by-Step Instructions:</h3>
<ol>
    <li>When prompted, select your preferred language (1 for English, 2 for Arabic).</li>
    <li>Enter the name of the city you want to search in.</li>
    <li>Select the type of location you are looking for from the provided list.</li>
    <li>The script will fetch the results and save them to an Excel file named <code>places_data.xlsx</code> in the current directory.</li>
</ol>

<h2>Configuration</h2>
<p>Replace <code>YOUR_GOOGLE_PLACES_API_KEY</code> with your actual Google Places API key in the script:</p>
<pre><code>api_key = 'YOUR_GOOGLE_PLACES_API_KEY'</code></pre>

<h2>Requirements</h2>
<ul>
    <li>Python 3.x</li>
    <li>Requests library</li>
    <li>Pandas library</li>
    <li>XlsxWriter library</li>
    <li>Colorama library</li>
</ul>

<h2>License</h2>
<p>This project is licensed under the MIT License. See the LICENSE file for more details.</p>

<h2>Contact</h2>
<p>For any inquiries or issues, please contact <a href="mailto:your-email@example.com">your-email@example.com</a>.</p>

</body>
</html>
