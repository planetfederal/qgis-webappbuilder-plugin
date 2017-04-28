.. _hosting_wab:

Hosting a WAB app
=================

You can easily host a Web app created with |current_plugin| using any web
hosting environment, like IIS or Apache. You can also use services like
Amazon AWS.

Hosting a WAB web app using AWS Console
---------------------------------------

#. Go to https://aws.amazon.com/ and create an aws account that will be
   used to host your web application.

#. Login to the AWS Management Console here: https://console.aws.amazon.com

#. Open the host a static website wizard either by clicking the link found on
   the AWS Management Console home page, then clicking the, :guilabel:`New
   site` link or by visiting this link directly:
   https://console.aws.amazon.com/quickstart-website/new

#. Use your preferred tool to create a zip archive of the :file:`webapp`
   directory that was created by the |current_plugin| plugin.

#. Back in the AWS Management Console, name your Web app, select the option to
   :guilabel:`Upload a zip file with your own code` and upload the zip file
   you created in the previous step. AWS will now publish and distribute
   your website to their content delivery network. You can follow their
   instructions to associate a domain name with your site or simply use the url
   found under the :guilabel:`Content delivery network` heading to distribute
   your new Web app!
