# Databricks notebook source

def transform_data(data):
    return [value * 2 for value in data]


def calculate_total(data):
    return sum(data)


data = [10, 20, 30, 40, 50]

transformed_data = transform_data(data)

total = calculate_total(transformed_data)


print("====================================")
print("Databricks CI/CD Demo")
print("====================================")

print(f"Input data       : {data}")
print(f"Transformed data : {transformed_data}")
print(f"Total            : {total}")

print("====================================")
print("Execution completed successfully")
print("====================================")
