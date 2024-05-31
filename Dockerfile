# Step 1: Pull the base image
FROM public.ecr.aws/lambda/python:3.11

# Step 2: Copy requirements.txt
COPY ./requirements.txt ${LAMBDA_TASK_ROOT}

# Step 3: Install the specified packages
RUN pip install -r requirements.txt

# Step 4: Copy function code
COPY ./ ${LAMBDA_TASK_ROOT}

# Step 5: Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]