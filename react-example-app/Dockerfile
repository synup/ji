FROM node:12.6.0-alpine
RUN apk add bash
ARG app_dir=/opt/app
WORKDIR ${app_dir}
COPY "react-example-app/package*.json" "react-example-app/yarn*" "${app_dir}/"
RUN yarn install
COPY react-example-app ${app_dir}
RUN yarn build
COPY APP-RELEASE APP-RELEASE
RUN printf "\nBUILD TIMESTAMP: \"$(date)\"\n" >> APP-RELEASE
CMD yarn start