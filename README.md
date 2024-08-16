## Inspiration

At first glance, we knew that 123Loadboard's challenge was for us. The implication of a real-world issue to be solved in our short hackathon session meant that we knew that our code could mirror the potential of what was available in the real world. With this in mind we embarked on our implementation of the notification system and threw in our own touch!

## What it does

GoodLuckTruck is an innovative platform designed to optimize freight matching for truckers. It intelligently connects truck drivers with the most suitable loads using a combination of geospatial data and advanced filtering algorithms. The system takes into account factors such as distance, profitability, and route efficiency. Truckers receive tailored load suggestions through a notification system that can be customized to their preferences, whether via SMS or in-app notifications. The platform's front-end interfaces, both on web and mobile, provide users with interactive maps that display the best routes from their current location to the pickup point, and from there to the load's drop-off destination. This comprehensive approach ensures that truckers can make informed decisions quickly and efficiently, leading to optimized routes, reduced fuel consumption, and maximized earnings.

## How we built it

We built our project in parallel with a python based backend, a swift based external mobile client and a react based internal web client. For our backend, we first parse from the MQTT streams, we store the trucks and loads in a custom implementation of KD-Trees optimized for geospatial coordinates. After this, we run the data through our custom filtering code which will take into account parameters such as a google maps API informed distance calculation and our calculated profits in order to determine the best loads to push out as a notification. Our notification system works with both an sms and an on client notification, such that the user can choose the style of notification they wish to have. Our frontends both use map libraries with custom routing and distance logic in order to display the optimal route from their location to the pickup and finally to the load drop-off destination.

## Challenges we ran into

Early on, we ran into challenges regarding the data structure we used. While our implementation of KD-Trees would typically be adequate for coordinates on a cartesian plane, we did not take into account that geospatial coordinates were on a globe. This meant that our euclidean distance based approach would not produce the best results. Even so, very late into the project, we resolved this issue with the implementation of the Haversine formula, a formula that enables the approximation of distances of two coordinates while taking into account of our Earth shaped as a globe.

## Accomplishments that we're proud of

We are proud of our output of not only the backend algorithm, but of our web socket connectivity as well as our development of two frontend clients based on the web and for mobile. From the backend side, we are proud that we came up with the use of a maps API in order to calculate the exact route distance from the truck to the origin and finally the destination.

## What we learned

From the backend, we learned a lot about different data structures that can efficiently handle geospatial coordinate sorted objects, web sockets for connectivity with clients and the MQTT protocol. In the frontend, this was the first time on both the web app and the mobile app that we ever used map based libraries and their apis.

## What's next for GoodLuckTruck

Perhaps in the future, we can implement a weigh based, machine learning model which adapts the notifications to the trucker's preferences over time. In this way, the algorithm will learn the loads that the trucker is most likely to accept over time and only ever push them their most relevant notifications.
