# Use an official Ruby runtime as a parent image
FROM ruby:3.1.2

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update -qq && apt-get install -y nodejs postgresql-client

# Install Rails and other necessary dependencies
RUN gem install rails -v 7.0.0

# Install Redis (needed for ActionCable)
RUN apt-get install -y redis-server

# Add the Rails project to the Docker container
COPY . /app

# Install the required gems
RUN bundle install

# Precompile assets for production (you can skip this in development)
# RUN RAILS_ENV=production bundle exec rake assets:precompile

# Expose port 7001 for Rails server and ActionCable
EXPOSE 7001

# Start the Rails server on port 7001
CMD ["rails", "s", "-b", "0.0.0.0", "-p", "7001"]
