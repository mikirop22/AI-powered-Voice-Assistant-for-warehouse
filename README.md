# HackUPC

## What it does
Introducing our latest innovation: a voice assistant tailored for warehouse efficiency. This cutting-edge tool enables workers to verbally input various product names and quantities, generating a detailed list instantly. But the innovation doesn't stop there.

Upon compiling the list, it undergoes optimization using a route planner specifically designed for warehouse environments. This route planner calculates the most efficient path through the warehouse, minimizing travel time and maximizing productivity.

Through an intuitive interface, workers can visualize the layout of the warehouse and the optimized route to retrieve items. Picture a digital map highlighting the locations of each product within the warehouse, along with a highlighted path indicating the shortest distance to collect them all.

By leveraging our voice assistant alongside the route optimization feature, warehouse operations are streamlined, saving time and resources. 

## How we built it

Here's a more detailed explanation of how we built our solution:

We started by incorporating the 'speech_recognition' library, which enabled us to accurately recognize and interpret user input. This technology allowed warehouse workers to verbally input product names and quantities, streamlining the data entry process.

To facilitate seamless interaction with the user, we integrated the 'pydub' library. This allowed us to manipulate audio files and enhance the user experience during communication with the voice assistant.

Once we compiled the list of products along with their respective quantities, we conducted a thorough verification process to ensure the availability of the items in the warehouse. This involved cross-referencing the requested quantities with the current inventory.

Upon confirmation of inventory availability, we uploaded the finalized product list to Google Cloud. This cloud-based platform provided a centralized location for accessing and managing the inventory data, ensuring real-time synchronization and accessibility for warehouse workers.

With the product list readily available, warehouse workers could seamlessly retrieve it and initiate the process of finding the most efficient route to collect the requested items. Leveraging advanced route optimization algorithms, we calculated the shortest path through the warehouse, minimizing travel time and maximizing productivity.

Finally, to enhance usability and facilitate navigation within the warehouse, we developed an intuitive interface. This interface displayed the optimized route, highlighted the location of each item within the warehouse, and provided visual cues to guide workers along the designated path.

By integrating these technologies and implementing a user-friendly interface, we created a comprehensive solution that significantly improved efficiency and productivity in warehouse operations.

## Challenges we ran into
In developing our latest warehouse efficiency innovation, we faced challenges in integrating accurate voice recognition and optimizing route planning for complex warehouse layouts. We had to ensure the system could interpret diverse accents. Creating an intuitive interface for visualizing layouts and routes also required balancing complexity with simplicity. Despite these hurdles, our team persevered, resulting in a tool that enhances productivity and minimizes errors in warehouse management.

## What we learned
Most notably, we discovered a myriad of libraries for understanding speech input and facilitating communication with users. Exploring various libraries for natural language processing enabled us to decipher user commands accurately and efficiently. Additionally, we delved into numerous libraries for voice interaction, enhancing our understanding of speech recognition and synthesis.

Furthermore, we gained valuable insights into the realm of graphical user interface design. Thiss allowed us to create intuitive interfaces that seamlessly communicate optimized routes to warehouse workers. Understanding the nuances of raphical user interface design proved instrumental in crafting user-friendly experiences that enhance productivity and efficiency in warehouse environments.

## Folders explanation
In 'allistar', we have the files related to the virtual assistant for creating product lists from our database through voice. By running main_list.py, it can generate and send this list through our AI-powered virtual assistant. In the 'treballador' folder, we have files that read this created list and find the optimal path knowing the locations of the products, oriented towards the company's workers.
