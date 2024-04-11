# Deploying Kubernetes Files using kubectl

## Overview
This README provides instructions on how to deploy Kubernetes files using `kubectl` to manage your Kubernetes resources.

## Prerequisites
- You should have `kubectl` configured to connect to your Kubernetes cluster.
- If you want to test it locally you can use `minikube` to start a local Kubernetes cluster. Check minikube [documentation](https://minikube.sigs.k8s.io/docs/start/).

## Steps to Deploy Kubernetes Files
1. **Apply Deployment File:**
    ```
    kubectl apply -f ./k8 -R
    ```

2. **Check Deployment Status:**
This command will display the status of your deployments.
    ```
    kubectl get deployments
    ```

3. **Check Service Status:**
This command will show the status of your services, including cluster IP and ports.

    ```
    kubectl get services
    ```

4. **Test Deployment:**
- Verify that your services are running correctly by testing their endpoints using tools like `curl`. Or you can test locally using port-forwarding.
    ```
    kubectl port-forward <pod_name> <local_port>:<service_port>
    ```

5. **View Resource Usage:**
- To view resource usage metrics of your pods:  
  ```
  kubectl top pods
  ```
- To view resource usage metrics of your nodes:  
  ```
  kubectl top nodes
  ```

## Additional Notes
- Make sure to customize the deployment and service files based on your specific requirements.
- Monitor the resource usage of your pods and nodes regularly to ensure optimal performance.