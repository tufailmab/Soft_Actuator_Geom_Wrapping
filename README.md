<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
  <h1>Fiber Wrapping Geometry Generation Tool</h1>

  <p>This project provides a Python-based solution for generating fiber-wrapped geometry around a soft bending actuator. The script automates the creation of a semi-circular fiber structure and positions it in a 3D space for dynamic finite-element analysis (FEA).</p>

  <h2>Features</h2>
  <ul>
    <li><strong>Geometry Creation:</strong> Generates fiber paths wrapped around a semi-circular structure.</li>
    <li><strong>Customizable Parameters:</strong> Allows users to specify the actuator radius, length, fiber angle, and translation values.</li>
    <li><strong>Finite Element Preparation:</strong> Provides a ready-to-analyze geometric model for dynamic FEA.</li>
    <li><strong>3D Positioning:</strong> Translates and aligns the fiber geometry in the assembly space.</li>
  </ul>

  <h2>Usage Instructions</h2>
  <ol>
    <li>Ensure that Abaqus and the necessary Python environment are installed.</li>
    <li>Define key parameters for the actuator and fiber geometry in the script:
      <ul>
        <li><code>Radius_of_Actuator</code></li>
        <li><code>Length_of_Actuator</code></li>
        <li><code>Smoothen_wrapping</code></li>
        <li><code>delta_x, delta_y, delta_z</code></li>
      </ul>
    </li>
    <li>Run the script using Abaqus Python scripting environment:
      <pre><code>abaqus cae noGUI=your_script_name.py</code></pre>
    </li>
    <li>The fiber-wrapped geometry will be generated and displayed in the Abaqus viewport.</li>
  </ol>

  <h2>Requirements</h2>
  <ul>
    <li>Abaqus CAE</li>
    <li>Python (Abaqus scripting environment)</li>
    <li>NumPy</li>
  </ul>

  <h2>License</h2>
  <p>This project is licensed under the <strong>MIT License</strong>.</p>
  <p>You are free to use, modify, and distribute this software under the terms of the MIT License. If you use this software in your work, please provide appropriate credit to the developer.</p>

  <h2>Developer Information</h2>
  <ul>
    <li><strong>Developer:</strong> Tufail Mabood</li>
    <li><strong>Contact:</strong> <a href="https://wa.me/+923440907874" target="_blank">WhatsApp</a></li>
    <li><strong>Note:</strong> This tool is open-source. Contributions and improvements are welcome.</li>
  </ul>
</body>
