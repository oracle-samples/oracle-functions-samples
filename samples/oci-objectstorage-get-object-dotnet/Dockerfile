FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add GetObjects.csproj
RUN dotnet build GetObjects.csproj -c Release
RUN dotnet publish GetObjects.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "GetObjects.dll"]
CMD ["GetObjects:Function:function_handler"]