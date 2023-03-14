FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add ListInstance.csproj
RUN dotnet build ListInstance.csproj -c Release
RUN dotnet publish ListInstance.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "ListInstance.dll"]
CMD ["ListInstance:Function:function_handler"]