FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add ControlInstance.csproj
RUN dotnet build ControlInstance.csproj -c Release
RUN dotnet publish ControlInstance.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "ControlInstance.dll"]
CMD ["ControlInstance:Function:function_handler"]